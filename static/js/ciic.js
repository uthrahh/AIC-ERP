document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.marquee-wrap').forEach(function (wrap) {
        var track = wrap.querySelector('.marquee-track');
        if (track && track.children.length > 0) {
            var clone = track.innerHTML;
            track.innerHTML = clone + clone;
        }
    });
});
