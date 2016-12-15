var Glyph, ImageRGBA, ImageRGBAView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Glyph = require("./glyph");

ImageRGBAView = (function(superClass) {
  extend(ImageRGBAView, superClass);

  function ImageRGBAView() {
    return ImageRGBAView.__super__.constructor.apply(this, arguments);
  }

  ImageRGBAView.prototype._index_data = function() {
    return this._xy_index();
  };

  ImageRGBAView.prototype._set_data = function(source, arg) {
    var buf, buf8, canvas, color, ctx, flat, i, image_data, j, k, l, ref, ref1, results;
    if ((this.image_data == null) || this.image_data.length !== this.image.length) {
      this.image_data = new Array(this.image.length);
    }
    if ((this.width == null) || this.width.length !== this.image.length) {
      this.width = new Array(this.image.length);
    }
    if ((this.height == null) || this.height.length !== this.image.length) {
      this.height = new Array(this.image.length);
    }
    results = [];
    for (i = k = 0, ref = this.image.length; 0 <= ref ? k < ref : k > ref; i = 0 <= ref ? ++k : --k) {
      if (arg != null) {
        if (i !== arg) {
          continue;
        }
      }
      if (this.rows != null) {
        this.height[i] = this.rows[i];
        this.width[i] = this.cols[i];
      } else {
        this.height[i] = this.image[i].length;
        this.width[i] = this.image[i][0].length;
      }
      canvas = document.createElement('canvas');
      canvas.width = this.width[i];
      canvas.height = this.height[i];
      ctx = canvas.getContext('2d');
      image_data = ctx.getImageData(0, 0, this.width[i], this.height[i]);
      if (this.rows != null) {
        image_data.data.set(new Uint8ClampedArray(this.image[i]));
      } else {
        flat = _.flatten(this.image[i]);
        buf = new ArrayBuffer(flat.length * 4);
        color = new Uint32Array(buf);
        for (j = l = 0, ref1 = flat.length; 0 <= ref1 ? l < ref1 : l > ref1; j = 0 <= ref1 ? ++l : --l) {
          color[j] = flat[j];
        }
        buf8 = new Uint8ClampedArray(buf);
        image_data.data.set(buf8);
      }
      ctx.putImageData(image_data, 0, 0);
      this.image_data[i] = canvas;
      this.max_dw = 0;
      if (this.dw.units === "data") {
        this.max_dw = _.max(this.dw);
      }
      this.max_dh = 0;
      if (this.dh.units === "data") {
        results.push(this.max_dh = _.max(this.dh));
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  ImageRGBAView.prototype._map_data = function() {
    this.sw = this.sdist(this.renderer.xmapper, this.x, this.dw, 'edge', this.mget('dilate'));
    return this.sh = this.sdist(this.renderer.ymapper, this.y, this.dh, 'edge', this.mget('dilate'));
  };

  ImageRGBAView.prototype._render = function(ctx, indices, arg1) {
    var i, image_data, k, len, old_smoothing, sh, sw, sx, sy, y_offset;
    image_data = arg1.image_data, sx = arg1.sx, sy = arg1.sy, sw = arg1.sw, sh = arg1.sh;
    old_smoothing = ctx.getImageSmoothingEnabled();
    ctx.setImageSmoothingEnabled(false);
    for (k = 0, len = indices.length; k < len; k++) {
      i = indices[k];
      if (isNaN(sx[i] + sy[i] + sw[i] + sh[i])) {
        continue;
      }
      y_offset = sy[i];
      ctx.translate(0, y_offset);
      ctx.scale(1, -1);
      ctx.translate(0, -y_offset);
      ctx.drawImage(image_data[i], sx[i] | 0, sy[i] | 0, sw[i], sh[i]);
      ctx.translate(0, y_offset);
      ctx.scale(1, -1);
      ctx.translate(0, -y_offset);
    }
    return ctx.setImageSmoothingEnabled(old_smoothing);
  };

  ImageRGBAView.prototype.bounds = function() {
    var bb;
    bb = this.index.data.bbox;
    return [[bb[0], bb[2] + this.max_dw], [bb[1], bb[3] + this.max_dh]];
  };

  return ImageRGBAView;

})(Glyph.View);

ImageRGBA = (function(superClass) {
  extend(ImageRGBA, superClass);

  function ImageRGBA() {
    return ImageRGBA.__super__.constructor.apply(this, arguments);
  }

  ImageRGBA.prototype.default_view = ImageRGBAView;

  ImageRGBA.prototype.type = 'ImageRGBA';

  ImageRGBA.prototype.visuals = [];

  ImageRGBA.prototype.distances = ['dw', 'dh'];

  ImageRGBA.prototype.fields = ['image:array', '?rows', '?cols'];

  ImageRGBA.prototype.defaults = function() {
    return _.extend({}, ImageRGBA.__super__.defaults.call(this), {
      dilate: false,
      rows: null,
      cols: null
    });
  };

  return ImageRGBA;

})(Glyph.Model);

module.exports = {
  Model: ImageRGBA,
  View: ImageRGBAView
};
