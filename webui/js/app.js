'use strict';
const $ = (s, scope = document) => scope.querySelector(s);
const $$ = (s, scope = document) => [...scope.querySelectorAll(s)];
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
} [c]));
const fmt = s => s ? new Date(`${s}T12:00:00`).toLocaleDateString('es-PE', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
}) : '';
const state = {
    page: 'dashboard',
    stations: [],
    types: [],
    songs: [],
    services: [],
    proposal: [],
    configIds: [],
    configType: null,
    chosenType: null,
    chosenDate: new Date().toLocaleDateString('en-CA')
};
const title = {
    dashboard: 'Dashboard',
    selection: 'Generar programa',
    songs: 'Canciones',
    stations: 'Estaciones',
    types: 'Tipos de programa',
    history: 'Programas'
};

async function api(name, ...args) {
    if (!window.pywebview?.api) throw new Error('El puente PyWebView no está disponible. Ejecuta main.py.');
    const result = await window.pywebview.api[name](...args);
    if (!result?.ok) throw new Error(result?.error || 'No se completó la operación.');
    return result.data;
}

function toast(message, error = false) {
    const el = $('#toast');
    el.textContent = message;
    el.className = error ? 'error' : '';
    el.style.display = 'block';
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => el.style.display = 'none', 3400);
}
async function task(fn) {
    try {
        await fn();
    } catch (e) {
        console.error(e);
        toast(e.message || String(e), true);
    }
}
async function refresh() {
    const data = await api('initial_data');
    Object.assign(state, data);
}

function go(page) {
    state.page = page;
    $('#pageTitle').textContent = title[page];
    $$('.nav-item').forEach(el => el.classList.toggle('active', el.dataset.page === page));
    render();
}

function header(text, action = '') {
    return `<div class="page-heading"><h2>${text}</h2><div class="actions">${action}</div></div>`;
}
const btn = (text, act, style = '') => `<button type="button" class="btn ${style}" data-action="${act}">${text}</button>`;
const empty = txt => `<div class="empty">${esc(txt)}</div>`;
const tag = active => `<span class="status ${active ? '' : 'off'}">${active ? 'Activo' : 'Inactivo'}</span>`;
const songName = s => s.tipo === 'himno' ? `${s.numero_himno ? '#' + s.numero_himno + ' · ' : ''}${s.titulo}` : s.titulo;
const options = (items, selected, fn, placeholder = 'Seleccionar...') => `<option value="">${placeholder}</option>` + items.map(x => `<option value="${x.id}" ${Number(selected) === Number(x.id) ? 'selected' : ''}>${esc(fn(x))}</option>`).join('');

function table(head, body) {
    return `<div class="table-wrap"><table class="data-table"><thead><tr>${head.map(x => `<th>${esc(x)}</th>`).join('')}</tr></thead><tbody>${body || `<tr><td colspan="${head.length}">${empty('No hay registros.')}</td></tr>`}</tbody></table></div>`;
}

function openModal(html) {
    const div = document.createElement('div');
    div.className = 'modal-overlay';
    div.id = 'modalOverlay';
    div.innerHTML = `<div class="modal" role="dialog" aria-modal="true">${html}</div>`;
    document.body.appendChild(div);
    div.addEventListener('click', e => {
        if (e.target === div) closeModal();
    });
}

function closeModal() {
    $('#modalOverlay')?.remove();
}

function field(label, id, value = '', type = 'text', extra = '') {
    return `<div class="field"><label for="${id}">${label}</label><input class="input" type="${type}" id="${id}" value="${esc(value)}" ${extra}></div>`;
}

function dashboard() {
    const recent = state.services.slice(0, 4).map(s => `<button class="card-link" data-action="view-service" data-id="${s.id}"><span><strong>${esc(s.program_type_name)}</strong><br><span class="small muted">${fmt(s.fecha)}</span></span><span class="small muted">${s.station_count} estaciones</span></button>`).join('') || empty('Aún no existen programas registrados.');
    return `<div class="mb-8"><p class="muted text-sm">Organiza tu servicio</p><h2 class="mt-1 text-2xl font-semibold tracking-tight">Prepara el próximo culto.</h2></div>
    <div class="hero"><p class="mini" style="letter-spacing:.15em;color:#a5b4fc;text-transform:uppercase">Nuevo programa</p><h3>Generar programa de culto</h3><p>Selecciona el tipo de culto y genera las canciones para cada estación. Puedes revisar la propuesta antes de guardarla.</p>${btn('Generar programa →', 'navigate-selection', 'primary')}</div>
    <div class="grid-two" style="margin-top:24px"><div class="panel"><div class="panel-head"><strong>Programas recientes</strong></div><div class="panel-body">${recent}${btn('Ver historial', 'navigate-history')}</div></div>
    <div class="panel"><div class="panel-head"><strong>Administración</strong></div><div class="panel-body">${[['songs', '♫', 'Canciones'], ['stations', '☷', 'Estaciones'], ['types', '▤', 'Tipos de programa']].map(x => `<button class="card-link" data-action="navigate-${x[0]}"><span>${x[1]} &nbsp; ${x[2]}</span><span>→</span></button>`).join('')}</div></div></div>`;
}

function stations() {
    const rows = state.stations.map(s => `<tr><td>${s.id}</td><td>${esc(s.nombre)}</td><td>${tag(s.activo)}</td><td class="nowrap"><button class="btn small" data-action="edit-station" data-id="${s.id}">Editar</button> <button class="btn small" data-action="toggle-station" data-id="${s.id}">${s.activo ? 'Desactivar' : 'Activar'}</button></td></tr>`).join('');
    return header('Estaciones', btn('+ Nueva estación', 'add-station', 'primary')) + `<div class="panel">${table(['ID', 'Estación', 'Estado', 'Acciones'], rows)}</div>`;
}

function types() {
    const rows = state.types.map(t => `<tr><td>${t.id}</td><td>${esc(t.nombre)}</td><td>${tag(t.activo)}</td><td class="nowrap"><button class="btn small" data-action="configure-type" data-id="${t.id}">Estaciones</button> <button class="btn small" data-action="edit-type" data-id="${t.id}">Editar</button> <button class="btn small" data-action="toggle-type" data-id="${t.id}">${t.activo ? 'Desactivar' : 'Activar'}</button></td></tr>`).join('');
    return header('Tipos de programa', btn('+ Nuevo tipo', 'add-type', 'primary')) + `<div class="panel">${table(['ID', 'Tipo de programa', 'Estado', 'Acciones'], rows)}</div>`;
}

function songs() {
    return header('Canciones', btn('+ Nueva canción', 'add-song', 'primary')) + `<div class="panel"><div class="panel-head flex-line"><input id="songSearch" class="input search-input" placeholder="Buscar canción o número..."><select id="songFilter" class="input search-input"><option value="">Todas las estaciones</option>${options(state.stations, null, s => s.nombre, '').replace('<option value=""> </option>', '')}</select></div><div id="songsTable"></div></div>`;
}

function drawSongTable() {
    const query = ($('#songSearch')?.value || '').trim().toLocaleLowerCase();
    const station = $('#songFilter')?.value || '';
    const list = state.songs.filter(s => (!station || String(s.station_id) === station) && (`${s.titulo} ${s.numero_himno || ''} ${s.station_name}`.toLocaleLowerCase().includes(query)));
    $('#songsTable').innerHTML = table(['ID', 'Título', 'Tipo', 'Referencia', 'Estación', 'Estado', 'Acciones'], list.map(s => `<tr><td>${s.id}</td><td>${esc(s.titulo)}</td><td>${esc(s.tipo)}${s.numero_himno ? ' #' + s.numero_himno : ''}</td><td>${esc(s.referencia)}</td><td>${esc(s.station_name)}</td><td>${tag(s.activo)}</td><td class="nowrap"><button class="btn small" data-action="edit-song" data-id="${s.id}">Editar</button> <button class="btn small" data-action="toggle-song" data-id="${s.id}">${s.activo ? 'Desactivar' : 'Activar'}</button></td></tr>`).join(''));
}

function selection() {
    const active = state.types.filter(x => x.activo);
    let rows = '';
    if (state.proposal.length) {
        rows = table(['#', 'Estación', 'Canción seleccionada', 'Referencia'], state.proposal.map((p, i) => `<tr><td>${i + 1}</td><td>${esc(p.station_name)}</td><td><select class="input selection-song" data-index="${i}"><option value="">Sin canción disponible</option>${(p.candidates || []).map(s => `<option value="${s.id}" ${Number(p.song_id) === Number(s.id) ? 'selected' : ''}>${esc(songName(s))}</option>`).join('')}</select></td><td>${p.song_id ? esc(p.referencia || '—') : '<span class="status off">Sin canción</span>'}</td></tr>`).join(''));
    }
    return header('Generar programa') + `<div class="panel"><div class="panel-head"><strong>Datos del culto</strong></div><div class="panel-body"><div class="form-grid"><div class="field"><label>Tipo de programa</label><select id="selectionType" class="input">${options(active, state.chosenType, t => t.nombre)}</select></div>${field('Fecha del culto', 'selectionDate', state.chosenDate, 'date')}</div><div class="form-footer">${btn('Generar propuesta', 'generate', 'primary')}</div></div></div>
  ${state.proposal.length ? `<div class="panel" style="margin-top:22px"><div class="panel-head"><strong>Propuesta de canciones</strong><p class="small muted" style="margin:6px 0 0">Puedes reemplazar cualquier canción antes de confirmar. Solo se registran las canciones confirmadas.</p></div>${rows}<div class="panel-body"><div class="form-footer">${btn('Regenerar', 'generate')}${btn('Confirmar y guardar', 'confirm', 'primary')}</div></div></div>` : ''}`;
}

function history() {
    const rows = state.services.map(s => `<tr><td>${s.id}</td><td>${fmt(s.fecha)}</td><td>${esc(s.program_type_name)}</td><td>${s.station_count}</td><td><button class="btn small" data-action="view-service" data-id="${s.id}">Ver detalle</button></td></tr>`).join('');
    return header('Historial de programas', btn('Actualizar', 'refresh-history')) + `<div class="panel">${table(['ID', 'Fecha', 'Programa', 'Canciones', 'Acción'], rows)}</div>`;
}

function render() {
    const screen = {
        dashboard,
        stations,
        types,
        songs,
        selection,
        history
    } [state.page];
    $('#content').innerHTML = screen();
    if (state.page === 'songs') drawSongTable();
}

function editName(entity, record) {
    const isStation = entity === 'station';
    openModal(`<h3>${record ? 'Editar' : 'Nuevo'} ${isStation ? 'estación' : 'tipo de programa'}</h3><form id="nameForm">${field('Nombre', 'editName', record?.nombre || '', 'text', 'required maxlength="150"')}<div class="form-footer">${btn('Cancelar', 'close-modal')}<button class="btn primary" type="submit">Guardar</button></div></form>`);
    $('#nameForm').addEventListener('submit', e => {
        e.preventDefault();
        task(async () => {
            await api(isStation ? 'save_station' : 'save_type', {
                id: record?.id || null,
                nombre: $('#editName').value
            });
            closeModal();
            await refresh();
            render();
            toast('Guardado correctamente.');
        });
    });
}

function editSong(song) {
    const active = state.stations.filter(s => s.activo || s.id === song?.station_id);
    openModal(`<h3>${song ? 'Editar' : 'Nueva'} canción</h3><form id="songForm" class="stack">${field('Título', 'editSongTitle', song?.titulo || '', 'text', 'required maxlength="250"')}<div class="form-grid"><div class="field"><label>Tipo</label><select id="editSongType" class="input"><option value="himno" ${song?.tipo === 'himno' ? 'selected' : ''}>Himno</option><option value="alabanza" ${song?.tipo === 'alabanza' ? 'selected' : ''}>Alabanza</option></select></div>${field('Número de himno', 'editSongNumber', song?.numero_himno || '', 'number', 'min="1"')}</div><div class="field"><label>Referencia</label><input class="input" id="editSongReference" disabled></div><div class="field"><label>Estación</label><select class="input" id="editSongStation" required>${options(active, song?.station_id, s => s.nombre)}</select></div><div class="form-footer">${btn('Cancelar', 'close-modal')}<button class="btn primary" type="submit">Guardar</button></div></form>`);
    const updateType = () => {
        const hymn = $('#editSongType').value === 'himno';
        $('#editSongNumber').disabled = !hymn;
        $('#editSongReference').value = hymn ? 'Himnario' : 'Folder';
        if (!hymn) $('#editSongNumber').value = '';
    };
    $('#editSongType').addEventListener('change', updateType);
    updateType();
    $('#songForm').addEventListener('submit', e => {
        e.preventDefault();
        task(async () => {
            await api('save_song', {
                id: song?.id || null,
                titulo: $('#editSongTitle').value,
                tipo: $('#editSongType').value,
                numero_himno: $('#editSongNumber').value || null,
                station_id: Number($('#editSongStation').value)
            });
            closeModal();
            await refresh();
            render();
            toast('Canción guardada.');
        });
    });
}
async function configure(id) {
    const type = state.types.find(t => t.id === id);
    state.configType = type;
    state.configIds = (await api('get_type_stations', id)).map(x => Number(x.station_id));
    renderConfig();
}

function renderConfig() {
    const type = state.configType;
    const available = state.stations.filter(s => s.activo && !state.configIds.includes(s.id));
    openModal(`<h3>Estaciones · ${esc(type.nombre)}</h3><p class="small muted" style="margin-bottom:15px">Ordena las estaciones según el desarrollo del culto.</p><div class="stack" id="orderItems">${state.configIds.map((id, i) => { const s = state.stations.find(x => x.id === id); return `<div class="order-item"><span>${i + 1}. ${esc(s?.nombre || 'Estación eliminada')}</span><div class="buttons"><button class="btn small" data-action="move-config" data-index="${i}" data-dir="-1" ${i === 0 ? 'disabled' : ''}>↑</button><button class="btn small" data-action="move-config" data-index="${i}" data-dir="1" ${i === state.configIds.length - 1 ? 'disabled' : ''}>↓</button><button class="btn small danger" data-action="remove-config" data-index="${i}">×</button></div></div>`; }).join('') || empty('Este programa no tiene estaciones.')}</div><div class="flex-line" style="margin-top:18px"><select class="input" id="addConfigSelect" style="flex:1">${options(available, null, s => s.nombre)}</select>${btn('Agregar', 'add-config')}</div><div class="form-footer">${btn('Cancelar', 'close-modal')}${btn('Guardar configuración', 'save-config', 'primary')}</div>`);
}
async function makeProposal() {
    const type = Number($('#selectionType').value);
    const date = $('#selectionDate').value;
    if (!type || !date) throw new Error('Selecciona un tipo de programa y una fecha.');
    state.chosenType = type;
    state.chosenDate = date;
    const proposal = await api('generate', type);
    for (const p of proposal) {
        p.candidates = await api('songs_by_station', p.station_id);
    }
    state.proposal = proposal;
    render();
    if (!proposal.length) toast('El programa no tiene estaciones configuradas.', true);
    else toast('Propuesta generada.');
}
async function confirmProposal() {
    if (!state.proposal.length) throw new Error('Primero genera una propuesta.');
    const missing = state.proposal.filter(p => !p.song_id);
    if (missing.length) throw new Error(`Faltan canciones en: ${missing.map(x => x.station_name).join(', ')}`);
    if (!confirm('¿Confirmar y guardar este culto?')) return;
    const id = await api('confirm', {
        fecha: state.chosenDate,
        program_type_id: state.chosenType,
        selection: state.proposal.map(p => ({
            station_id: p.station_id,
            station_name: p.station_name,
            song_id: p.song_id
        }))
    });
    state.proposal = [];
    await refresh();
    go('history');
    toast(`Culto #${id} guardado correctamente.`);
}
async function viewService(id) {
    const result = await api('get_service', id);
    const s = result.service;
    openModal(`<h3>${esc(s.program_type_name)}</h3><p class="muted small" style="margin-bottom:15px">${fmt(s.fecha)} · Registro #${s.id}</p>${table(['Estación', 'Canción', 'Referencia'], result.songs.map(x => `<tr><td>${esc(x.station_name)}</td><td>${esc(x.song_title)}</td><td>${esc(x.referencia)} ${x.numero_himno ? '#' + x.numero_himno : ''}</td></tr>`).join(''))}<div class="form-footer">${btn('Cerrar', 'close-modal')}</div>`);
}

$('#navigation').addEventListener('click', e => {
    const b = e.target.closest('[data-page]');
    if (b) go(b.dataset.page);
});
document.addEventListener('click', e => {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    const a = el.dataset.action,
        id = Number(el.dataset.id);
    task(async () => {
        if (a.startsWith('navigate-')) return go(a.slice(9));
        if (a === 'close-modal') return closeModal();
        if (a === 'add-station') return editName('station');
        if (a === 'edit-station') return editName('station', state.stations.find(x => x.id === id));
        if (a === 'add-type') return editName('type');
        if (a === 'edit-type') return editName('type', state.types.find(x => x.id === id));
        if (a === 'add-song') return editSong();
        if (a === 'edit-song') return editSong(state.songs.find(x => x.id === id));
        if (a.startsWith('toggle-')) {
            const type = a.slice(7);
            const item = (type === 'station' ? state.stations : type === 'type' ? state.types : state.songs).find(x => x.id === id);
            if (!item) return;
            if (!confirm(`${item.activo ? 'Desactivar' : 'Activar'} ${item.nombre || item.titulo}?`)) return;
            await api(`set_${type}_active`, id, !item.activo);
            await refresh();
            render();
            return toast('Estado actualizado.');
        }
        if (a === 'configure-type') return configure(id);
        if (a === 'move-config') {
            const i = Number(el.dataset.index),
                j = i + Number(el.dataset.dir);
            [state.configIds[i], state.configIds[j]] = [state.configIds[j], state.configIds[i]];
            closeModal();
            return renderConfig();
        }
        if (a === 'remove-config') {
            state.configIds.splice(Number(el.dataset.index), 1);
            closeModal();
            return renderConfig();
        }
        if (a === 'add-config') {
            const n = Number($('#addConfigSelect').value);
            if (!n) return;
            state.configIds.push(n);
            closeModal();
            return renderConfig();
        }
        if (a === 'save-config') {
            await api('save_type_stations', state.configType.id, state.configIds);
            closeModal();
            return toast('Configuración guardada.');
        }
        if (a === 'generate') return makeProposal();
        if (a === 'confirm') return confirmProposal();
        if (a === 'view-service') return viewService(id);
        if (a === 'refresh-history') {
            await refresh();
            render();
            return toast('Historial actualizado.');
        }
    });
});
document.addEventListener('input', e => {
    if (e.target.matches('#songSearch,#songFilter')) drawSongTable();
    if (e.target.id === 'selectionDate') state.chosenDate = e.target.value;
});
document.addEventListener('change', e => {
    if (e.target.id === 'selectionType') {
        state.chosenType = Number(e.target.value) || null;
        state.proposal = [];
        render();
    }
    if (e.target.matches('.selection-song')) {
        const p = state.proposal[Number(e.target.dataset.index)];
        const chosen = p.candidates.find(s => s.id === Number(e.target.value));
        if (chosen) {
            Object.assign(p, {
                song_id: chosen.id,
                song_title: chosen.titulo,
                tipo: chosen.tipo,
                referencia: chosen.referencia,
                numero_himno: chosen.numero_himno,
                available: true
            });
        } else {
            Object.assign(p, {
                song_id: null,
                song_title: null,
                tipo: null,
                referencia: null,
                numero_himno: null,
                available: false
            });
        }
        render();
    }
    if (e.target.id === 'songFilter') drawSongTable();
});
const theme = localStorage.getItem('theme') === 'light' ? 'light' : 'dark';
document.body.classList.replace('theme-dark', `theme-${theme}`);
$('#themeToggle').textContent = theme === 'light' ? '☾' : '☼';
$('#themeToggle').addEventListener('click', () => {
    const light = document.body.classList.contains('theme-light');
    document.body.classList.replace(light ? 'theme-light' : 'theme-dark', light ? 'theme-dark' : 'theme-light');
    localStorage.setItem('theme', light ? 'dark' : 'light');
    $('#themeToggle').textContent = light ? '☼' : '☾';
});
async function boot() {
    try {
        await refresh();
        state.chosenType = state.types.find(t => t.activo)?.id || null;
        render();
    } catch (err) {
        $('#content').innerHTML = `<div class="panel panel-body"><h2>No se pudo iniciar</h2><p class="muted">${esc(err.message)}</p></div>`;
    }
}
window.addEventListener('pywebviewready', boot);
// También muestra una explicación si el HTML se abre directamente en un navegador.
setTimeout(() => {
    if (!window.pywebview?.api && $('#content')?.textContent.includes('Cargando')) $('#content').innerHTML = empty('Inicia la aplicación ejecutando python main.py para conectarla con SQLite.');
}, 1800);