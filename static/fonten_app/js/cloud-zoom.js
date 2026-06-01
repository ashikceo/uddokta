document.addEventListener('DOMContentLoaded', function() {
  var wrapper = document.getElementById('mainImageWrapper');
  var mainImg = document.getElementById('mainProductImage');
  var lens = document.getElementById('imageZoomLens');
  var result = document.getElementById('imageZoomResult');
  if (!wrapper || !mainImg || !lens || !result) return;

  result.style.backgroundImage = "url('" + mainImg.src + "')";

  wrapper.addEventListener('mouseenter', function() {
    lens.style.display = 'block';
    result.style.display = 'block';
  });

  wrapper.addEventListener('mousemove', function(e) {
    var rect = wrapper.getBoundingClientRect();
    var x = e.clientX - rect.left;
    var y = e.clientY - rect.top;
    var lw = lens.offsetWidth / 2;
    var lh = lens.offsetHeight / 2;
    x = Math.max(lw, Math.min(x, rect.width - lw));
    y = Math.max(lh, Math.min(y, rect.height - lh));
    lens.style.left = (x - lw) + 'px';
    lens.style.top = (y - lh) + 'px';

    var ratio = result.offsetWidth / lens.offsetWidth;
    var bgX = (x - lw) * ratio;
    var bgY = (y - lh) * ratio;
    result.style.backgroundSize = (rect.width * ratio) + 'px ' + (rect.height * ratio) + 'px';
    result.style.backgroundPosition = '-' + bgX + 'px -' + bgY + 'px';
  });

  wrapper.addEventListener('mouseleave', function() {
    lens.style.display = 'none';
    result.style.display = 'none';
  });

  var thumbGallery = document.getElementById('thumbnailGallery');
  if (thumbGallery) {
    thumbGallery.addEventListener('click', function(e) {
      var thumb = e.target.closest('.thumb-item');
      if (!thumb) return;
      var src = thumb.dataset.src;
      if (!src) return;
      mainImg.src = src;
      result.style.backgroundImage = "url('" + src + "')";
      thumbGallery.querySelectorAll('.thumb-item').forEach(function(t) {
        t.classList.remove('active');
      });
      thumb.classList.add('active');
    });
  }
});
