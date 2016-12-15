var Marker, Square, SquareView, _, bokehgl,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

bokehgl = require("../glyphs/bokehgl");

SquareView = (function(superClass) {
  extend(SquareView, superClass);

  function SquareView() {
    return SquareView.__super__.constructor.apply(this, arguments);
  }

  SquareView.prototype._init_gl = function(gl) {
    return this.glglyph = new bokehgl.SquareGLGlyph(gl, this);
  };

  SquareView.prototype._render = function(ctx, indices, arg) {
    var angle, i, j, len, results, size, sx, sy;
    sx = arg.sx, sy = arg.sy, size = arg.size, angle = arg.angle;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sx[i] + sy[i] + size[i] + angle[i])) {
        continue;
      }
      ctx.beginPath();
      ctx.translate(sx[i], sy[i]);
      if (angle[i]) {
        ctx.rotate(angle[i]);
      }
      ctx.rect(-size[i] / 2, -size[i] / 2, size[i], size[i]);
      if (angle[i]) {
        ctx.rotate(-angle[i]);
      }
      if (this.visuals.fill.do_fill) {
        this.visuals.fill.set_vectorize(ctx, i);
        ctx.fill();
      }
      if (this.visuals.line.do_stroke) {
        this.visuals.line.set_vectorize(ctx, i);
        ctx.stroke();
      }
      results.push(ctx.translate(-sx[i], -sy[i]));
    }
    return results;
  };

  return SquareView;

})(Marker.View);

Square = (function(superClass) {
  extend(Square, superClass);

  function Square() {
    return Square.__super__.constructor.apply(this, arguments);
  }

  Square.prototype.default_view = SquareView;

  Square.prototype.type = 'Square';

  return Square;

})(Marker.Model);

module.exports = {
  Model: Square,
  View: SquareView
};
