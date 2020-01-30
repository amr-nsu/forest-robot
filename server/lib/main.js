const robot1 = 'http://10.42.0.1:8000'

function setSensorValue(response, elem) {
    const hud = document.getElementById('hud').contentDocument;
    const item = hud.getElementById(elem);
    item.textContent = response;
}

function responseCallback(response, elem) {
    const item = document.getElementById(elem);
    item.innerHTML = response;
}

function request(cmd, elem='') {
    const req = new XMLHttpRequest();
    req.open('GET', cmd, true);
    req.onload = function() {
        if (req.status == 200) {
            if (elem == 'course' || elem == 'altitude') {
                setSensorValue(req.responseText, elem);
            }
            else if (elem != '') {
                responseCallback(req.responseText, elem);
            }
        }
    }
    req.send();
}

function databaseTimeoutCallback() {
    const cmd = robot1 + '/cmd=d';
    request(cmd, 'database');
    setTimeout('databaseTimeoutCallback();', 2000);
}

function courseTimeoutCallback() {
    const cmd = robot1 + '/cmd=c';
    request(cmd, 'course');
    setTimeout('courseTimeoutCallback();', 1000);
}

function altitudeBaroTimeoutCallback() {
    const cmd = robot1 + '/cmd=b';
    request(cmd, 'altitude');
    setTimeout('altitudeBaroTimeoutCallback();', 2000);
}

function main() {
    courseTimeoutCallback();
    databaseTimeoutCallback();
    altitudeBaroTimeoutCallback();
}
