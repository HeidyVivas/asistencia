// Variables globales
const API_BASE = '/api';
let currentUser = null;
let aprendices = [];
let faltasData = [];

// Obtener token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Inicializar cuando carga la página
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadDashboard();
});

// Inicializar listeners de eventos
function initializeEventListeners() {
    const navButtons = document.querySelectorAll('.nav-menu button');
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            navButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const section = this.dataset.section;
            loadSection(section);
        });
    });
}

// Cargar sección
function loadSection(section) {
    const content = document.getElementById('content');
    
    switch(section) {
        case 'aprendices':
            loadAprendices();
            break;
        case 'asistencias':
            loadAsistencias();
            break;
        case 'faltas':
            loadFaltas();
            break;
        case 'excusas':
            loadExcusas();
            break;
        case 'reglamento':
            loadReglamento();
            break;
        default:
            loadDashboard();
    }
}

// Cargar Dashboard
function loadDashboard() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card">
            <h2>📊 Dashboard</h2>
            <div id="dashboard-stats">
                <div class="form-group">
                    <h3>Bienvenido al Sistema de Asistencia</h3>
                    <p>Sistema de gestión de asistencia, faltas y excusas para aprendices.</p>
                </div>
                <div class="form-group">
                    <h3>Funcionalidades:</h3>
                    <ul>
                        <li>Registrar aprendices</li>
                        <li>Registrar asistencias</li>
                        <li>Gestionar faltas</li>
                        <li>Presentar excusas</li>
                        <li>Ver reglamento</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
}

// Cargar Aprendices
function loadAprendices() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card">
            <h2>👥 Aprendices</h2>
            <form id="aprendizForm">
                <div class="form-group">
                    <label for="username">Usuario:</label>
                    <input type="text" id="username" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" required>
                </div>
                <div class="form-group">
                    <label for="first_name">Nombre:</label>
                    <input type="text" id="first_name" required>
                </div>
                <div class="form-group">
                    <label for="last_name">Apellido:</label>
                    <input type="text" id="last_name" required>
                </div>
                <button type="submit">Registrar Aprendiz</button>
            </form>
            <div id="aprendicesList" class="table-container" style="margin-top: 30px;"></div>
        </div>
    `;
    
    document.getElementById('aprendizForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createAprendiz();
    });
    
    fetchAprendices();
}

// Cargar Asistencias
function loadAsistencias() {
    const content = document.getElementById('content');
    
    // Obtener fecha de hoy en formato YYYY-MM-DD
    const hoy = new Date();
    const fechaMax = hoy.toISOString().split('T')[0];
    
    content.innerHTML = `
        <div class="card">
            <h2>✓ Asistencias</h2>
            <form id="asistenciaForm">
                <div class="form-group">
                    <label for="aprendiz">Aprendiz:</label>
                    <select id="aprendiz" required>
                        <option value="">Seleccionar aprendiz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="fecha">Fecha:</label>
                    <input type="date" id="fecha" max="${fechaMax}" required>
                </div>
                <div class="form-group">
                    <label for="estado">Estado:</label>
                    <select id="estado" required>
                        <option value="presente">Presente</option>
                        <option value="ausente">Ausente</option>
                        <option value="tardanza">Tardanza</option>
                    </select>
                </div>
                <button type="submit">Registrar Asistencia</button>
            </form>
            <div id="asistenciasList" class="table-container" style="margin-top: 30px;"></div>
        </div>
    `;
    
    document.getElementById('asistenciaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createAsistencia();
    });
    
    fetchAsistencias();
    setTimeout(() => updateAprendicesSelects(), 100);
}

// Cargar Faltas
function loadFaltas() {
    const content = document.getElementById('content');
    
    // Obtener fecha de hoy en formato YYYY-MM-DD
    const hoy = new Date();
    const fechaMax = hoy.toISOString().split('T')[0];
    
    content.innerHTML = `
        <div class="card">
            <h2>✗ Faltas</h2>
            <form id="faltaForm">
                <div class="form-group">
                    <label for="falta-aprendiz">Aprendiz:</label>
                    <select id="falta-aprendiz" required>
                        <option value="">Seleccionar aprendiz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="falta-fecha">Fecha de Falta:</label>
                    <input type="date" id="falta-fecha" max="${fechaMax}" required>
                </div>
                <div class="form-group">
                    <label for="es-tardanza">¿Es tardanza?</label>
                    <input type="checkbox" id="es-tardanza">
                </div>
                <button type="submit">Registrar Falta</button>
            </form>
            <div id="faltasList" class="table-container" style="margin-top: 30px;"></div>
        </div>
    `;
    
    document.getElementById('faltaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createFalta();
    });
    
    fetchFaltas();
    setTimeout(() => updateAprendicesSelects(), 100);
}

// Cargar Excusas
function loadExcusas() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card">
            <h2>📄 Excusas</h2>
            <form id="excusaForm">
                <div class="form-group">
                    <label for="excusa-aprendiz">Aprendiz:</label>
                    <select id="excusa-aprendiz" required>
                        <option value="">Seleccionar aprendiz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="excusa-falta">Falta:</label>
                    <select id="excusa-falta" required>
                        <option value="">Seleccionar falta</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="tipo-documento">Tipo de Documento:</label>
                    <input type="text" id="tipo-documento" placeholder="Ej: NOTA_MEDICA" required>
                </div>
                <div class="form-group">
                    <label for="descripcion">Descripción:</label>
                    <textarea id="descripcion" rows="4"></textarea>
                </div>
                <button type="submit">Presentar Excusa</button>
            </form>
            <div id="excusasList" class="table-container" style="margin-top: 30px;"></div>
        </div>
    `;
    
    document.getElementById('excusaForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createExcusa();
    });
    
    fetchExcusas();
    fetchFaltas();
    setTimeout(() => { updateAprendicesSelects(); updateFaltasSelects(); }, 150);
}

// Cargar Reglamento
function loadReglamento() {
    const content = document.getElementById('content');
    content.innerHTML = `
        <div class="card">
            <h2>📋 Reglamento</h2>
            <form id="reglamentoForm">
                <div class="form-group">
                    <label for="nombre">Nombre:</label>
                    <input type="text" id="nombre" required>
                </div>
                <div class="form-group">
                    <label for="descripcion-regl">Descripción:</label>
                    <textarea id="descripcion-regl" rows="4" required></textarea>
                </div>
                <div class="form-group">
                    <label for="dias-habiles">Días Hábiles para Excusa:</label>
                    <input type="number" id="dias-habiles" value="3" required>
                </div>
                <button type="submit">Guardar Reglamento</button>
            </form>
            <div id="reglamentoList" class="table-container" style="margin-top: 30px;"></div>
        </div>
    `;
    
    document.getElementById('reglamentoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        createReglamento();
    });
    
    fetchReglamento();
}

// Funciones de API
async function fetchAsistencias() {
    try {
        const response = await fetch(`${API_BASE}/asistencias/`);
        const data = await response.json();
        displayAsistencias(data);
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al cargar asistencias', 'error');
    }
}

async function createAsistencia() {
    const aprendiz = document.getElementById('aprendiz').value;
    const fecha = document.getElementById('fecha').value;
    const estado = document.getElementById('estado').value;
    
    if (!aprendiz || !fecha || !estado) {
        showAlert('Por favor completa todos los campos', 'error');
        return;
    }
    
    // VALIDACIÓN: Rechazar fechas en el futuro
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    const fecha_ingresada = new Date(fecha);
    
    if (fecha_ingresada > hoy) {
        showAlert('❌ No se puede registrar una asistencia en una fecha futura.\nFecha ingresada: ' + fecha + '\nHoy: ' + hoy.toISOString().split('T')[0], 'error');
        return;
    }
    
    console.log('Enviando asistencia:', { aprendiz: parseInt(aprendiz), fecha, estado });
    
    try {
        const response = await fetch(`${API_BASE}/asistencias/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                aprendiz: parseInt(aprendiz),
                fecha: fecha,
                estado: estado
            })
        });
        
        // Verificar si la respuesta es JSON
        const contentType = response.headers.get('content-type');
        let responseData;
        
        if (contentType && contentType.includes('application/json')) {
            responseData = await response.json();
        } else {
            const text = await response.text();
            console.error('Respuesta no JSON. Status:', response.status);
            console.error('Contenido:', text.substring(0, 500));
            showAlert('Error del servidor: ' + text.substring(0, 200), 'error');
            return;
        }
        
        if (response.ok) {
            showAlert('✓ Asistencia registrada correctamente', 'success');
            document.getElementById('asistenciaForm').reset();
            fetchAsistencias();
        } else {
            console.error('Error:', responseData);
            showAlert('❌ Error: ' + (responseData.error || JSON.stringify(responseData)), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('❌ Error: ' + error.message, 'error');
    }
}

async function fetchFaltas() {
    try {
        const response = await fetch(`${API_BASE}/faltas/`);
        const data = await response.json();
        faltasData = data;
        displayFaltas(data);
        updateFaltasSelects();
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al cargar faltas', 'error');
    }
}

async function createFalta() {
    const aprendiz = document.getElementById('falta-aprendiz').value;
    const fecha_falta = document.getElementById('falta-fecha').value;
    const es_tardanza = document.getElementById('es-tardanza').checked;
    
    // VALIDACIÓN: Rechazar fechas en el futuro
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    const fecha_ingresada = new Date(fecha_falta);
    
    if (fecha_ingresada > hoy) {
        showAlert('❌ No se puede registrar una falta en una fecha futura.\nFecha ingresada: ' + fecha_falta + '\nHoy: ' + hoy.toISOString().split('T')[0], 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/faltas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                aprendiz: parseInt(aprendiz),
                fecha_falta: fecha_falta,
                es_tardanza: es_tardanza
            })
        });
        
        if (response.ok) {
            showAlert('✓ Falta registrada correctamente', 'success');
            document.getElementById('faltaForm').reset();
            fetchFaltas();
        } else {
            const data = await response.json();
            showAlert('❌ Error: ' + (data.error || JSON.stringify(data)), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('❌ Error de conexión', 'error');
    }
}

async function fetchExcusas() {
    try {
        const response = await fetch(`${API_BASE}/excusas/`);
        const data = await response.json();
        displayExcusas(data);
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al cargar excusas', 'error');
    }
}

async function createExcusa() {
    const falta = document.getElementById('excusa-falta').value;
    const aprendiz = document.getElementById('excusa-aprendiz').value;
    const tipo_documento = document.getElementById('tipo-documento').value;
    const descripcion = document.getElementById('descripcion').value;
    
    try {
        const response = await fetch(`${API_BASE}/excusas/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                falta: falta,
                aprendiz: aprendiz,
                tipo_documento: tipo_documento,
                descripcion: descripcion
            })
        });
        
        if (response.ok) {
            showAlert('Excusa presentada correctamente', 'success');
            document.getElementById('excusaForm').reset();
            fetchExcusas();
        } else {
            const data = await response.json();
            showAlert('Error: ' + JSON.stringify(data), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión', 'error');
    }
}

async function fetchReglamento() {
    try {
        const response = await fetch(`${API_BASE}/reglamento/`);
        const data = await response.json();
        displayReglamento(data);
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error al cargar reglamento', 'error');
    }
}

async function createReglamento() {
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion-regl').value;
    const dias_habiles = document.getElementById('dias-habiles').value;
    
    try {
        const response = await fetch(`${API_BASE}/reglamento/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                nombre: nombre,
                descripcion: descripcion,
                dias_habiles_para_excusa: dias_habiles
            })
        });
        
        if (response.ok) {
            showAlert('Reglamento guardado correctamente', 'success');
            document.getElementById('reglamentoForm').reset();
            fetchReglamento();
        } else {
            const data = await response.json();
            showAlert('Error: ' + JSON.stringify(data), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión', 'error');
    }
}

// Funciones de visualización
function displayAsistencias(data) {
    const list = document.getElementById('asistenciasList');
    
    if (!data || data.length === 0) {
        list.innerHTML = '<p>No hay asistencias registradas</p>';
        return;
    }
    
    let html = '<table><thead><tr><th>Aprendiz</th><th>Fecha</th><th>Estado</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += `<tr>
            <td>${item.aprendiz_nombre || item.aprendiz}</td>
            <td>${item.fecha}</td>
            <td><span class="status-badge status-${item.estado.toLowerCase()}">${item.estado}</span></td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    list.innerHTML = html;
}

function displayFaltas(data) {
    const list = document.getElementById('faltasList');
    
    if (!data || data.length === 0) {
        list.innerHTML = '<p>No hay faltas registradas</p>';
        return;
    }
    
    let html = '<table><thead><tr><th>Aprendiz</th><th>Fecha</th><th>Tardanza</th><th>Estado</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += `<tr>
            <td>${item.aprendiz}</td>
            <td>${item.fecha_falta}</td>
            <td>${item.es_tardanza ? 'Sí' : 'No'}</td>
            <td><span class="status-badge status-${item.estado.toLowerCase()}">${item.estado}</span></td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    list.innerHTML = html;
}

function displayExcusas(data) {
    const list = document.getElementById('excusasList');
    
    if (!data || data.length === 0) {
        list.innerHTML = '<p>No hay excusas presentadas</p>';
        return;
    }
    
    let html = '<table><thead><tr><th>Aprendiz</th><th>Tipo</th><th>Estado</th><th>Presentación</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += `<tr>
            <td>${item.aprendiz}</td>
            <td>${item.tipo_documento}</td>
            <td><span class="status-badge status-${item.estado.toLowerCase()}">${item.estado}</span></td>
            <td>${item.fecha_presentacion || ''}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    list.innerHTML = html;
}

function displayReglamento(data) {
    const list = document.getElementById('reglamentoList');
    
    if (!data || data.length === 0) {
        list.innerHTML = '<p>No hay reglamentos registrados</p>';
        return;
    }
    
    let html = '<table><thead><tr><th>Nombre</th><th>Descripción</th><th>Días Hábiles</th></tr></thead><tbody>';
    
    data.forEach(item => {
        html += `<tr>
            <td>${item.nombre}</td>
            <td>${item.descripcion.substring(0, 50)}...</td>
            <td>${item.dias_habiles_para_excusa}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    list.innerHTML = html;
}

// Utilidades
function showAlert(message, type) {
    const content = document.getElementById('content');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    content.insertBefore(alert, content.firstChild);
    
    setTimeout(() => alert.remove(), 5000);
}

// Funciones de Aprendices
async function fetchAprendices() {
    try {
        const response = await fetch(`${API_BASE}/usuarios/aprendices/`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        aprendices = data;
        displayAprendices(data);
        updateAprendicesSelects();
    } catch (error) {
        console.error('Error al cargar aprendices:', error);
        showAlert('Error al cargar aprendices: ' + error.message, 'error');
    }
}

async function createAprendiz() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const first_name = document.getElementById('first_name').value;
    const last_name = document.getElementById('last_name').value;
    
    if (!username || !email || !first_name || !last_name) {
        showAlert('Por favor completa todos los campos', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/usuarios/aprendices/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                username: username,
                email: email,
                first_name: first_name,
                last_name: last_name,
                password: 'aprendiz123'
            })
        });
        
        const responseData = await response.json();
        
        if (response.ok) {
            showAlert('Aprendiz registrado correctamente', 'success');
            document.getElementById('aprendizForm').reset();
            await fetchAprendices();
        } else {
            const errorMessage = JSON.stringify(responseData);
            console.error('Error response:', errorMessage);
            showAlert('Error al registrar aprendiz: ' + errorMessage, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error de conexión: ' + error.message, 'error');
    }
}

function displayAprendices(data) {
    const list = document.getElementById('aprendicesList');
    
    if (!list) {
        console.error('No se encontró elemento con id "aprendicesList"');
        return;
    }
    
    if (!data || data.length === 0) {
        list.innerHTML = '<p style="text-align: center; color: #999; padding: 20px;">No hay aprendices registrados aún</p>';
        return;
    }
    
    let html = '<table><thead><tr><th>Usuario</th><th>Email</th><th>Nombre</th><th>Apellido</th></tr></thead><tbody>';
    
    data.forEach((item) => {
        html += `<tr>
            <td>${item.username || ''}</td>
            <td>${item.email || ''}</td>
            <td>${item.first_name || ''}</td>
            <td>${item.last_name || ''}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    list.innerHTML = html;
}

function updateAprendicesSelects() {
    const selects = document.querySelectorAll('#aprendiz, #falta-aprendiz, #excusa-aprendiz');
    
    selects.forEach((select) => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">Seleccionar aprendiz</option>';
        
        aprendices.forEach(aprendiz => {
            const option = document.createElement('option');
            option.value = aprendiz.id;
            option.textContent = `${aprendiz.first_name} ${aprendiz.last_name} (${aprendiz.username})`;
            select.appendChild(option);
        });
        
        if (currentValue) {
            select.value = currentValue;
        }
    });
}

function updateFaltasSelects() {
    const select = document.getElementById('excusa-falta');
    if (!select) return;
    const currentValue = select.value;
    select.innerHTML = '<option value="">Seleccionar falta</option>';
    
    faltasData.forEach(falta => {
        const option = document.createElement('option');
        option.value = falta.id;
        // Mostrar aprendiz y fecha para identificar la falta
        option.textContent = `${falta.aprendiz} - ${falta.fecha_falta}`;
        select.appendChild(option);
    });
    
    if (currentValue) select.value = currentValue;
}
