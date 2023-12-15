const cmds_freq = 5;

const handle_max_radius = 50;
const handle_min_radius = 12;

const handle_min_angle = 0;
const handle_max_angle = 0.7;

var socket = null;

var handle_start_pos = null;

var last_update = null;

const handle_elem = document.getElementById("pad_handle");
const status_txt = document.getElementById("status_txt");

function get_time() {
    return (new Date()).getTime();
}

function set_status(msg) {
    status_txt.textContent = msg;
}

function error(data) {
    const msg = generic_to_str(data);
    console.error(msg);
    set_status("Error: " + msg);
}

function info(data) {
    const msg = generic_to_str(data);
    console.info(msg);
    set_status("Info: " + msg);
}

function send(data) {
    if (socket === null) {
        return;
    }
    console.log("Send: ", JSON.stringify(data));
    socket.send(JSON.stringify(data))
}

function send_freewheel() {
    send({op: 'f'});
}

function send_brake() {
    send({op: 'b'});
}

function send_move(speed, turn) {
    send({op: 'm', data: {turn: turn, speed: speed}});
}

function update_motion(handle_pos, bypass_timeout = false) {
    const current_ts = get_time();
    if (!bypass_timeout && last_update !== null && (current_ts - last_update) < (1000 / cmds_freq))
        return;
    last_update = current_ts;

    if (handle_pos === null) {
        send_freewheel();
        return;
    }

    let [x, y] = handle_pos;

    const length = Math.sqrt(x*x + y*y);
    const speed = (length < handle_min_radius) ? 0 : ((length - handle_min_radius) / (handle_max_radius - handle_min_radius));

    if (speed <= 0) {
        send_brake();
    } else {
        let angle = Math.atan2(y, x) / Math.PI * 2;
        let turn = (angle < 0) ? (angle + 1) : (1 - angle);
        if (turn > 0)
            turn = (Math.min(Math.max(turn, handle_min_angle), handle_max_angle) - handle_min_angle) / (handle_max_angle - handle_min_angle);
        else
            turn = -(Math.min(Math.max(-turn, handle_min_angle), handle_max_angle) - handle_min_angle) / (handle_max_angle - handle_min_angle);
        send_move((y > 0) ? -speed : speed, turn);
    }
}

function generic_to_str(data) {
    msg = null;
    if (typeof data === "string") {
        msg = data;
    } else {
        msg = JSON.stringify(data);
    }
    return msg;
}

function keypressed(elem, ev) {
    if(ev.keyCode == 13) {
        if (elem === ip_input) {
            connect();
        }
    }
}

const ip_input = document.getElementById("ip_input");
const ip_regex = new RegExp(/^([0-9]+\.){3}[0-9]+$/);

function connect() {
    const ip = ip_input.value;

    if (!ip_regex.test(ip)) {
        error("Invalid ip '" + ip + "'");
        return;
    }

    info("Connecting ...");

    // Create WebSocket connection
    socket = new WebSocket("ws://" + ip + ":8005");

    // Connection opened
    socket.addEventListener("open", (event) => {
        info("Connected successfully");
    });

    // Listen for messages
    socket.addEventListener("message", (event) => {
        console.log("Receive message: " + event.data);
    });

    socket.addEventListener("error", (event) => {
        error("Some WebSocket error");
    });
}

function handle_grab(x, y) {
    handle_start_pos = [x, y];
    update_motion([0, 0], true);
    if (socket === null)
    {
        error("Not connected");
    }
}

function handle_move(x, y) {
    if (handle_start_pos !== null) {
        let dx = x - handle_start_pos[0];
        let dy = y - handle_start_pos[1];
        let k = Math.sqrt(dx*dx + dy*dy);
        if (k < handle_min_radius) {
            k = 0;
        } else {
            k = Math.min(handle_max_radius, k) / k;
        }
        dx *= k;
        dy *= k;
        handle_elem.style.left = dx.toString() + "px";
        handle_elem.style.top = dy.toString() + "px";
        update_motion([dx, dy]);
    }
}

function handle_ungrab() {
    handle_elem.style.left = 0;
    handle_elem.style.top = 0;
    if (handle_start_pos !== null)
        update_motion(null, true);
    handle_start_pos = null;
}

function setup() {
    handle_elem.addEventListener("mousedown", (ev) => {
        handle_grab(ev.pageX, ev.pageY);
    });
    document.addEventListener("mousemove", (ev) => {
        handle_move(ev.pageX, ev.pageY);
    });
    document.addEventListener("mouseup", (ev) => {
        handle_ungrab();
    });
    handle_elem.addEventListener("touchstart", (ev) => {
        const touch = ev.touches.item(0);
        handle_grab(touch.screenX, touch.screenY);
    });
    document.addEventListener("touchmove", (ev) => {
        const touch = ev.touches.item(0);
        handle_move(touch.screenX, touch.screenY);
    });
    document.addEventListener("touchend", (ev) => {
        handle_ungrab();
    });
}
