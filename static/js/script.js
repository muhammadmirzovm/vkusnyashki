(function () {
  "use strict";


  const meta = document.getElementById('sse-metadata');
  if (!meta) return;
  const sseUrl = meta.dataset.sseUrl;
  const monitorId = meta.dataset.monitorId;


  function q(sel, root=document) { return root.querySelector(sel); }
  function qAll(sel, root=document) { return Array.from(root.querySelectorAll(sel)); }


  function selectItemForRow(itemEl) {
    if (!itemEl) return;
    const row = itemEl.closest('.menu-row');
    if (!row) return;

    const imgEl = q('.preview-img', row);
    const priceEl = q('.preview-price-tag', row);
    const titleEl = q('.preview-title', row);

    const photo = itemEl.getAttribute('data-photo-url') || '';
    const price = itemEl.getAttribute('data-price') || 0;
    const name = (itemEl.querySelector('.item-name') || {}).textContent || '';


    if (photo && photo.trim() !== '') {
      if (imgEl) imgEl.src = photo;
    }

    if (priceEl) priceEl.textContent = `$${Number(price || 0).toFixed(2)}`;
    if (titleEl) titleEl.textContent = name;

    row.querySelectorAll('.item.selected').forEach(el => el.classList.remove('selected'));
    itemEl.classList.add('selected');
  }


  function attachItemHandlers(root=document) {
    qAll('.item', root).forEach(item => {

      if (item.__menu_bound) return;
      item.addEventListener('click', function () { selectItemForRow(item); }, { passive: true });
      item.__menu_bound = true;
    });
  }


  document.addEventListener('DOMContentLoaded', function () {
    attachItemHandlers();

    qAll('.menu-row').forEach(row => {
      const first = row.querySelector('.item:not(.unavailable)');
      if (first) {
        selectItemForRow(first);
      } else {

        const priceEl = q('.preview-price-tag', row);
        const titleEl = q('.preview-title', row);
        if (priceEl) priceEl.textContent = '$0.00';
        if (titleEl) titleEl.textContent = '';
      }
    });
  });


  let es = null;
  if (sseUrl) {
    try {
      es = new EventSource(sseUrl);
    } catch (err) {
      console.error('EventSource failed to initialize', err);
    }
  }


  function createItemElement(payload) {
    const li = document.createElement('li');
    li.className = 'item' + (payload.is_available === false ? ' unavailable' : '');
    li.id = `food-${payload.id}`;
    li.setAttribute('data-food-id', payload.id);
    li.setAttribute('data-category-id', payload.category_id);
    li.setAttribute('data-photo-url', payload.photo_url || '');
    li.setAttribute('data-price', payload.price || '');

    const nameSpan = document.createElement('span');
    nameSpan.className = 'item-name';
    nameSpan.textContent = payload.name || '';

    const priceSpan = document.createElement('span');
    priceSpan.className = 'item-price';
    priceSpan.textContent = (payload.price !== undefined && payload.price !== null) ? Number(payload.price).toFixed(2) : '';

    li.appendChild(nameSpan);
    li.appendChild(priceSpan);

    li.addEventListener('click', function () { selectItemForRow(li); }, { passive: true });
    li.__menu_bound = true;
    return li;
  }

  function handleFoodCreated(payload) {
    const list = document.getElementById(`category-${payload.category_id}-list`);
    if (!list) return;

    if (document.getElementById(`food-${payload.id}`)) return;
    const li = createItemElement(payload);
    list.appendChild(li);

    const row = list.closest('.menu-row');

    if (row && !row.querySelector('.item.selected') && !li.classList.contains('unavailable')) {
      selectItemForRow(li);
    }
  }

function handleFoodUpdated(payload) {
  const el = document.getElementById(`food-${payload.id}`);


  if (!el) {
    handleFoodCreated(payload);
    return;
  }


  if (payload.is_available === false) {
    const row = el.closest('.menu-row');
    const wasSelected = el.classList.contains('selected');

    el.remove();


    if (wasSelected && row) {
      const next = row.querySelector('.item:not(.unavailable)');
      if (next) {
        selectItemForRow(next);
      } else {

        const priceElRow = q('.preview-price-tag', row);
        const titleElRow = q('.preview-title', row);
        if (priceElRow) priceElRow.textContent = '$0.00';
        if (titleElRow) titleElRow.textContent = '';

      }
    }


    return;
  }


  el.setAttribute('data-photo-url', payload.photo_url || '');
  el.setAttribute('data-price', payload.price || '');

  const nameEl = el.querySelector('.item-name');
  const priceEl = el.querySelector('.item-price');

  if (nameEl) nameEl.textContent = payload.name || '';
  if (priceEl) priceEl.textContent = (payload.price !== undefined && payload.price !== null) ? Number(payload.price).toFixed(2) : '';
  el.classList.remove('unavailable');
  const row = el.closest('.menu-row');
  if (row && el.classList.contains('selected')) {
    selectItemForRow(el);
  }
}


  function handleFoodDeleted(payload) {
    const el = document.getElementById(`food-${payload.id}`);
    if (!el) return;
    const row = el.closest('.menu-row');
    const wasSelected = el.classList.contains('selected');
    el.remove();

    if (wasSelected && row) {
      const next = row.querySelector('.item:not(.unavailable)');
      if (next) {
        selectItemForRow(next);
      } else {
        const priceEl = q('.preview-price-tag', row);
        const titleEl = q('.preview-title', row);
        if (priceEl) priceEl.textContent = '$0.00';
        if (titleEl) titleEl.textContent = '';
      }
    }
  }

  if (es) {
    es.onmessage = function (e) {
      if (!e.data) return;
      let msg;
      try { msg = JSON.parse(e.data); } catch (err) { return; }
      if (!msg || msg.type !== 'food_update') return;

      const action = msg.action;
      const p = msg.payload || {};

      if (p.monitor_id && String(p.monitor_id) !== String(monitorId)) return;

      if (action === 'created') handleFoodCreated(p);
      else if (action === 'updated') handleFoodUpdated(p);
      else if (action === 'deleted') handleFoodDeleted(p);
    };

    es.onerror = function (err) {
      console.warn('SSE error', err);
    };
  }


  window.__menuPreview = {
    selectById: function(id) {
      const el = document.getElementById('food-' + id);
      if (el) selectItemForRow(el);
    }
  };


  window.__menuPreview._attachHandlers = function () { attachItemHandlers(); };




})();
