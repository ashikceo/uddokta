document.addEventListener('DOMContentLoaded', function() {

    // ===== Image Gallery / Thumbnail Switching =====
    var thumbGallery = document.getElementById('thumbnailGallery');
    var mainImage = document.getElementById('mainProductImage');
    if (thumbGallery && mainImage) {
        thumbGallery.querySelectorAll('.thumb-item').forEach(function(thumb) {
            thumb.addEventListener('click', function() {
                var active = thumbGallery.querySelector('.thumb-item.active');
                if (active) active.classList.remove('active');
                this.classList.add('active');
                mainImage.src = this.dataset.src;
                mainImage.setAttribute('data-zoom-image', this.dataset.src);
                // Update active zoom result if visible
                var result = document.getElementById('imageZoomResult');
                if (result && result.style.display !== 'none') {
                    result.style.backgroundImage = "url('" + this.dataset.src + "')";
                }
            });
        });
    }

    // ===== Image Zoom (Magnifier) =====
    var wrapper = document.getElementById('mainImageWrapper');
    var lens = document.getElementById('imageZoomLens');
    var result = document.getElementById('imageZoomResult');
    if (wrapper && mainImage && lens && result) {
        wrapper.addEventListener('mouseenter', function() {
            var zoomSrc = mainImage.dataset.zoomImage || mainImage.src;
            if (!zoomSrc) return;
            lens.style.display = 'block';
            result.style.display = 'block';
            result.style.backgroundImage = "url('" + zoomSrc + "')";
            // Reposition result based on available space
            var rect = wrapper.getBoundingClientRect();
            var spaceRight = window.innerWidth - rect.right - 20;
            var spaceLeft = rect.left - 20;
            var resultW = Math.min(380, Math.max(spaceRight, spaceLeft, 200));
            result.style.width = resultW + 'px';
            result.style.height = resultW + 'px';
            result.style.left = '';
            result.style.right = '';
            if (spaceRight >= resultW + 15) {
                result.style.left = (rect.width + 15) + 'px';
            } else {
                result.style.right = (rect.width + 15) + 'px';
            }
        });
        wrapper.addEventListener('mouseleave', function() {
            lens.style.display = 'none';
            result.style.display = 'none';
        });
        wrapper.addEventListener('mousemove', function(e) {
            if (lens.style.display === 'none') return;
            var rect = wrapper.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;
            var lensW = lens.offsetWidth;
            var lensH = lens.offsetHeight;
            var lx = x - lensW / 2;
            var ly = y - lensH / 2;
            if (lx < 0) lx = 0;
            if (ly < 0) ly = 0;
            if (lx > rect.width - lensW) lx = rect.width - lensW;
            if (ly > rect.height - lensH) ly = rect.height - lensH;
            lens.style.left = lx + 'px';
            lens.style.top = ly + 'px';
            var ratio = 3;
            result.style.backgroundPosition = (-lx * ratio) + 'px ' + (-ly * ratio) + 'px';
            result.style.backgroundSize = (rect.width * ratio) + 'px ' + (rect.height * ratio) + 'px';
        });
    }

    // ===== Quantity Selector =====
    document.querySelectorAll('.qty-selector').forEach(function(selector) {
        var minus = selector.querySelector('.qty-minus');
        var plus = selector.querySelector('.qty-plus');
        var input = selector.querySelector('.qty-input');
        if (!minus || !plus || !input) return;
        var max = parseInt(input.getAttribute('max')) || 999;
        minus.addEventListener('click', function() {
            var val = parseInt(input.value) || 1;
            if (val > 1) { input.value = val - 1; }
        });
        plus.addEventListener('click', function() {
            var val = parseInt(input.value) || 1;
            if (val < max) { input.value = val + 1; }
        });
    });

    // ===== Sticky Add-to-Cart Bar =====
    var addToCartForm = document.getElementById('addToCartForm');
    var stickyBar = document.getElementById('stickyCartBar');
    if (addToCartForm && stickyBar) {
        var observer = new IntersectionObserver(function(entries) {
            stickyBar.classList.toggle('visible', !entries[0].isIntersecting);
        }, { threshold: 0, rootMargin: '0px 0px -60px 0px' });
        observer.observe(addToCartForm);

        // Sync sticky qty with main form qty
        var mainQty = document.getElementById('qtyInput');
        var stickyQty = stickyBar.querySelector('.qty-input');
        var stickyAddBtn = stickyBar.querySelector('.btn-sticky-cart');
        if (mainQty && stickyQty) {
            stickyBar.querySelectorAll('.qty-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    mainQty.value = stickyQty.value;
                });
            });
            stickyQty.addEventListener('change', function() {
                mainQty.value = this.value;
            });
        }
        if (stickyAddBtn && addToCartForm) {
            stickyAddBtn.addEventListener('click', function() {
                addToCartForm.querySelector('[type="submit"]').click();
            });
        }
    }

    // ===== Quick View Modal =====
    var modal = document.getElementById('quickViewModal');
    var modalBody = document.getElementById('quickViewBody');
    var modalClose = document.getElementById('quickViewClose');
    if (modal && modalBody && modalClose) {
        document.querySelectorAll('.quick-view-btn').forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                var productId = this.dataset.productId;
                if (!productId) return;
                modalBody.innerHTML = '<div style="text-align:center;padding:40px;"><i class="fa fa-spinner fa-spin fa-2x"></i><p>Loading...</p></div>';
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
                fetch('/quick-view/' + productId + '/')
                    .then(function(res) { return res.json(); })
                    .then(function(data) {
                        modalBody.innerHTML = data.html;
                        // Re-init qty selectors inside modal
                        modalBody.querySelectorAll('.qty-selector').forEach(function(sel) {
                            var minus = sel.querySelector('.qty-minus');
                            var plus = sel.querySelector('.qty-plus');
                            var inp = sel.querySelector('.qty-input');
                            if (minus && plus && inp) {
                                var mx = parseInt(inp.getAttribute('max')) || 999;
                                minus.addEventListener('click', function() {
                                    var v = parseInt(inp.value) || 1;
                                    if (v > 1) inp.value = v - 1;
                                });
                                plus.addEventListener('click', function() {
                                    var v = parseInt(inp.value) || 1;
                                    if (v < mx) inp.value = v + 1;
                                });
                            }
                        });
                    })
                    .catch(function() {
                        modalBody.innerHTML = '<p style="text-align:center;padding:20px;color:#e74847;">Failed to load product details.</p>';
                    });
            });
        });
        modalClose.addEventListener('click', function() {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        });
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    }

});
