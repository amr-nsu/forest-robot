const robot1 = 'http://10.42.0.1:8000'

function responseCallback(response, elem) {
    const element = document.getElementById(elem);
    element.innerHTML = response;
}

function request(cmd, elem='') {
    const req = new XMLHttpRequest();
    req.open('GET', cmd, true);
    req.onload = function() {
        if (req.status == 200 && elem != '') {
            responseCallback(req.responseText, elem);
        }
    }
    req.send();
}

function databaseTimeoutCallback() {
    const cmd = robot1 + '/cmd=d';
    request(cmd, 'database');
    setTimeout('databaseTimeoutCallback();', 5000);
}


function main() {
    databaseTimeoutCallback();
}
