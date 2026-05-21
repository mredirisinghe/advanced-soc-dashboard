async function loadStats(){

    const res = await fetch('/api/stats');

    const data = await res.json();

    document.getElementById("total").innerText = data.total;

    document.getElementById("critical").innerText = data.critical;

    document.getElementById("high").innerText = data.high;

    document.getElementById("medium").innerText = data.medium;
}

async function loadIncidents(){

    const res = await fetch('/api/incidents');

    const data = await res.json();

    let html = "";

    data.forEach(x => {

        html += `

        <tr>

        <td>${x.timestamp}</td>

        <td>${x.ip}</td>

        <td>${x.attack_type}</td>

        <td class="${x.severity}">
            ${x.severity}
        </td>

        <td>${x.mitre}</td>

        </tr>

        `;
    });

    document.getElementById("incident-body").innerHTML = html;
}

async function refreshAll(){

    await loadStats();

    await loadIncidents();
}

refreshAll();

setInterval(refreshAll, 3000);
