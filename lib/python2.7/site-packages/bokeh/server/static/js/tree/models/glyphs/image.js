var Glyph, Greys9, Image, ImageView, LinearColorMapper, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Glyph = require("../glyphs/glyph");

LinearColorMapper = require("../mappers/linear_color_mapper");

Greys9 = require('../../palettes/palettes').Greys9;

ImageView = (function(superClass) {
  extend(ImageView, superClass);

  function ImageView() {
    return ImageView.__super__.constructor.apply(this, arguments);
  }

  ImageView.prototype._index_data = function() {
    return this._xy_index();
  };

  ImageView.prototype._set_data = function() {
    var buf, buf8, canvas, cmap, ctx, i, image_data, img, j, ref, results;
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
    for (i = j = 0, ref = this.image.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
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
      cmap = this.mget('color_mapper');
      if (this.rows != null) {
        img = this.image[i];
      } else {
        img = _.flatten(this.image[i]);
      }
      buf = cmap.v_map_screen(img);
      buf8 = new Uint8ClampedArray(buf);
      image_data.data.set(buf8);
      ctx.putImageData(image_data, 0, 0);
      this.image_data[i] = canvas;
      this.max_dw = 0;
      if (this.dw.units === "data") {
        this.max_dw = _.max(this.dw);
      }
      this.max_dh = 0;
      if (this.dh.units === "data") {
        this.max_dh = _.max(this.dh);
      }
      results.push(this._xy_index());
    }
    return results;
  };

  ImageView.prototype._map_data = function() {
    this.sw = this.sdist(this.renderer.xmapper, this.x, this.dw, 'edge', this.mget('dilate'));
    return this.sh = this.sdist(this.renderer.ymapper, this.y, this.dh, 'edge', this.mget('dilate'));
  };

  ImageView.prototype._render = function(ctx, indices, arg) {
    var i, image_data, j, len, old_smoothing, sh, sw, sx, sy, y_offset;
    image_data = arg.image_data, sx = arg.sx, sy = arg.sy, sw = arg.sw, sh = arg.sh;
    old_smoothing = ctx.getImageSmoothingEnabled();
    ctx.setImageSmoothingEnabled(false);
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (image_data[i] == null) {
        continue;
      }
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

  ImageView.prototype.bounds = function() {
    var bb;
    bb = this.index.data.bbox;
    return [[bb[0], bb[2] + this.max_dw], [bb[1], bb[3] + this.max_dh]];
  };

  return ImageView;

})(Glyph.View);

Image = (function(superClass) {
  extend(Image, superClass);

  function Image() {
    return Image.__super__.constructor.apply(this, arguments);
  }

  Image.prototype.default_view = ImageView;

  Image.prototype.type = 'Image';

  Image.prototype.visuals = [];

  Image.prototype.distances = ['dw', 'dh'];

  Image.prototype.fields = ['image:array', '?rows', '?cols'];

  Image.prototype.defaults = function() {
    return _.extend({}, Image.__super__.defaults.call(this), {
      dilate: false,
      color_mapper: new LinearColorMapper.Model({
        palette: Greys9
      })
    });
  };

  return Image;

})(Glyph.Model);

module.exports = {
  Model: Image,
  View: ImageView
};
