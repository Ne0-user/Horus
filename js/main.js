/* =============================================
   SysMon Dashboard — dashboard.js
   ============================================= */

/* ── Sidebar Toggle ── */
const sidebar    = document.getElementById('sidebar');
const toggleBtn  = document.getElementById('toggleBtn');
const toggleIcon = document.getElementById('toggle-icon');

toggleBtn.addEventListener('click', () => {
    const collapsed = sidebar.classList.toggle('collapsed');
    toggleIcon.className = collapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left';
});

/* ── Nav Active ── */
function setActive(event, el) {
    event.preventDefault();
    document.querySelectorAll('.nav-item-link').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
}

/* ── Donut Chart ── */
const donutCtx = document.getElementById('donutChart').getContext('2d');
const centerText = {
    id: 'centerText',

    beforeDraw(chart){
        const {ctx, data} = chart;

        const dataset = data.datasets[0].data;

        const total = dataset.reduce((a,b)=> a+b, 0);

        const meta = chart.getDatasetMeta(0);
        const x = meta.data[0].x;
        const y = meta.data[0].y;

        ctx.save();

        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        ctx.fillStyle = '#fff';
        ctx.font = '700 30px sans-serif';

        ctx.fillText(total.toFixed(1), x, y-10);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';

        ctx.fillText('Total', x, y+20);

        ctx.restore();
    }
};

new Chart(donutCtx,{
    type:'doughnut',

    data:{
        labels:['Chrome','Electron','Python','Node.js','Otros'],

        datasets:[{
            data:[18,8,12,9,32],

            backgroundColor:[
                '#4f8ef7',
                '#38bdf8',
                '#a78bfa',
                '#4ade80',
                '#475569'
            ]
        }]
    },

    options:{
        responsive:false,
        cutout:'75%'
    },

    plugins:[centerText]
});

/* ── Line Chart ── */
const lineLabels = Array.from({ length: 60 }, (_, i) => {
    if (i === 0)  return '60s';
    if (i === 29) return '30s';
    if (i === 59) return '0s';
    return '';
});

function genInitial(base, noise) {
    return Array.from({ length: 60 }, () => base + (Math.random() - 0.5) * noise);
}

const lineCtx = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(lineCtx, {
    type: 'line',
    data: {
        labels: lineLabels,
        datasets: [
            {
                label: 'RAM usada %',
                data: genInitial(67, 8),
                borderColor: '#4f8ef7',
                backgroundColor: 'rgba(79,142,247,0.12)',
                fill: true, tension: 0.4, pointRadius: 0, borderWidth: 2
            },
            {
                label: 'Swap %',
                data: genInitial(22, 3),
                borderColor: '#a78bfa',
                backgroundColor: 'rgba(167,139,250,0.08)',
                fill: true, tension: 0.4, pointRadius: 0, borderWidth: 1.5,
                borderDash: [4, 3]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 200 },
        scales: {
            x: {
                ticks: { color: '#4a5568', font: { size: 10 }, maxRotation: 0 },
                grid:  { color: 'rgba(255,255,255,0.04)' },
                border:{ color: 'rgba(255,255,255,0.06)' }
            },
            y: {
                min: 50, max: 90,
                ticks: { color: '#4a5568', font: { size: 10 }, callback: v => v + '%' },
                grid:  { color: 'rgba(255,255,255,0.05)' },
                border:{ color: 'rgba(255,255,255,0.06)' }
            }
        },
        plugins: { legend: { display: false } }
    }
});

/* ── Helper: bounded random drift ── */
function drift(val, range, min = 0, max = 100) {
    return Math.max(min, Math.min(max, val + (Math.random() - 0.5) * range));
}

function crearTopProceso(datos){
    return `
        <div class="d-flex align-items-center gap-2">

            <div class="app-icon ${datos.iconColor} flex-shrink-0">
                <i class="${datos.icono}"></i>
            </div>

            <div class="flex-grow-1 min-w-0">

                <div class="d-flex align-items-center gap-2 flex-wrap">

                    <span class="app-name">${datos.nombre}</span>

                </div>

                <div class="app-pid">
                    PID ${datos.pid} · ${datos.procesos} procesos
                </div>

                <div class="app-bar-wrap mt-1">
                    <div
                        class="app-bar-fill"
                        id="${datos.idBarra}"
                        style="width:${datos.porcentaje}%;background:${datos.colorBarra}">
                    </div>
                </div>

            </div>

            <div class="app-mem flex-shrink-0" id="${datos.idMemoria}">
                ${datos.memoria}
            </div>

        </div>
    `;
}

/* ── Live State ── */
let usedPct   = 66.9;
let swapPct   = 15;
let chromeMem = 5.9;
let vscodeMem = 3.8;
let pythonMem = 2.5;
let nodeMem   = 1.9;

const apps = [
    {
        nombre:"Google Chrome",
        icono:"bi bi-browser-chrome",
        iconColor:"blue-icon",
        estado:"activo",
        pid:3812,
        procesos:34,
        porcentaje:80,
        colorBarra:"#4f8ef7",
        memoria:"5.9 GB",
        idBarra:"bar-chrome",
        idMemoria:"mem-chrome"
    },

    {
        nombre:"VS Code",
        icono:"bi bi-code-slash",
        iconColor:"cyan-icon",
        estado:"activo",
        pid:5241,
        procesos:6,
        porcentaje:54,
        colorBarra:"#38bdf8",
        memoria:"3.8 GB",
        idBarra:"bar-vscode",
        idMemoria:"mem-vscode"
    },

    {
        nombre:"Python 3.12",
        icono:"bi bi-filetype-py",
        iconColor:"purple-icon",
        estado:"activo",
        pid:8234,
        procesos:3,
        porcentaje:35,
        colorBarra:"#a78bfa",
        memoria:"2.5 GB",
        idBarra:"bar-python",
        idMemoria:"mem-python"
    }
];

const contenedor = document.getElementById("Top_procesos");

    apps.forEach(app => {
    contenedor.innerHTML += crearTopProceso(app);
});

/* ── Update Loop (every 1.2 s) ── */
setInterval(() => {

    /* Memory totals */
    usedPct = drift(usedPct, 1.5, 40, 90);
    swapPct = drift(swapPct, 0.6,  5, 40);

    const usedGB = (32 * usedPct / 100).toFixed(1);
    const freeGB = (32 - 32 * usedPct / 100).toFixed(1);
    const swapGB = (8  * swapPct  / 100).toFixed(1);

    document.getElementById('mem-used').textContent  = usedGB + ' GB';
    document.getElementById('mem-free').textContent  = freeGB + ' GB';
    document.getElementById('swap-used').textContent = swapGB + ' GB';
    document.getElementById('mem-pct').textContent   = usedPct.toFixed(1) + '% del total';

    document.getElementById('bar-total').style.width = usedPct + '%';
    document.getElementById('bar-used').style.width  = usedPct + '%';
    document.getElementById('bar-free').style.width  = (100 - usedPct) + '%';
    document.getElementById('bar-swap').style.width  = swapPct + '%';

    document.getElementById('donut-pct').textContent = usedPct.toFixed(1) + '%';

    /* Per-process memory */
    chromeMem = drift(chromeMem, 0.15, 4,   8);
    vscodeMem = drift(vscodeMem, 0.10, 2,   6);
    pythonMem = drift(pythonMem, 0.08, 1,   4);
    nodeMem   = drift(nodeMem,   0.06, 0.5, 3);

    document.getElementById('mem-chrome').textContent = chromeMem.toFixed(1) + ' GB';
    document.getElementById('mem-vscode').textContent = vscodeMem.toFixed(1) + ' GB';
    document.getElementById('mem-python').textContent = pythonMem.toFixed(1) + ' GB';
    document.getElementById('mem-node').textContent   = nodeMem.toFixed(1)   + ' GB';

    const maxMem = 7.4;
    document.getElementById('bar-chrome').style.width = Math.min(100, chromeMem / maxMem * 100).toFixed(1) + '%';
    document.getElementById('bar-vscode').style.width = Math.min(100, vscodeMem / maxMem * 100).toFixed(1) + '%';
    document.getElementById('bar-python').style.width = Math.min(100, pythonMem / maxMem * 100).toFixed(1) + '%';
    document.getElementById('bar-node').style.width   = Math.min(100, nodeMem   / maxMem * 100).toFixed(1) + '%';

    /* Page faults */
    const minor = Math.round(drift(2841, 300, 2000, 4000));
    const major = Math.round(drift(47,    12,   20,  100));
    const ratio = ((major / minor) * 100).toFixed(1);

    document.getElementById('faults-minor').innerHTML =
        minor.toLocaleString('es-MX') + ' <span class="faults-unit">menores/s</span>';
    document.getElementById('faults-major').innerHTML =
        major.toLocaleString('es-MX') + ' <span class="faults-unit">mayores/s</span>';
    document.getElementById('ratio-val').textContent = ratio + '%';

    /* Paging stats */
    document.getElementById('pag-activas').textContent =
        Math.round(drift(187432, 3000, 150000, 220000)).toLocaleString('es-MX');
    document.getElementById('pag-virtual').textContent =
        Math.round(drift(49810,  2000,  40000,  60000)).toLocaleString('es-MX');

    /* Scroll line chart */
    lineChart.data.datasets[0].data.shift(); lineChart.data.datasets[0].data.push(usedPct);
    lineChart.data.datasets[1].data.shift(); lineChart.data.datasets[1].data.push(swapPct + 10);
    lineChart.update('none');

}, 1200);
