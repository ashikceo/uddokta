function CountBack_slider(secs, id, type) {
    var d = Math.floor(secs / 86400);
    var h = Math.floor((secs % 86400) / 3600);
    var m = Math.floor((secs % 3600) / 60);
    var s = Math.floor(secs % 60);
    var display = d + "d " + h + "h " + m + "m " + s + "s";
    document.getElementById(id).innerHTML = display;
    if (secs > 0) {
        secs--;
        setTimeout(function() { CountBack_slider(secs, id, type); }, 1000);
    }
}
