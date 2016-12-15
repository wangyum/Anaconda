var Marker, Triangle, TriangleView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

TriangleView = (function(superClass) {
  extend(TriangleView, superClass);

  function TriangleView() {
    return TriangleView.__super__.constructor.apply(this, arguments);
  }

  TriangleView.prototype._render = function(ctx, indices, arg) {
    var a, angle, h, i, j, len, r, results, size, sx, sy;
    sx = arg.sx, sy = arg.sy, size = arg.size, angle = arg.angle;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sx[i] + sy[i] + size[i] + angle[i])) {
        continue;
      }
      a = size[i] * Math.sqrt(3) / 6;
      r = size[i] / 2;
      h = size[i] * Math.sqrt(3) / 2;
      ctx.beginPath();
      ctx.translate(sx[i], sy[i]);
      if (angle[i]) {
        ctx.rotate(angle[i]);
      }
      ctx.moveTo(-r, a);
      ctx.lineTo(r, a);
      ctx.lineTo(0, a - h);
      if (angle[i]) {
        ctx.rotate(-angle[i]);
      }
      ctx.translate(-sx[i], -sy[i]);
      ctx.closePath();
      if (this.visuals.fill.do_fill) {
        this.visuals.fill.set_vectorize(ctx, i);
        ctx.fill();
      }
      if (this.visuals.line.do_stroke) {
        this.visuals.line.set_vectorize(ctx, i);
        results.push(ctx.stroke());
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  return TriangleView;

})(Marker.View);

Triangle = (function(superClass) {
  extend(Triangle, superClass);

  function Triangle() {
    return Triangle.__super__.constructor.apply(this, arguments);
  }

  Triangle.prototype.default_view = TriangleView;

  Triangle.prototype.type = 'Triangle';

  return Triangle;

})(Marker.Model);

module.exports = {
  Model: Triangle,
  View: TriangleView
};
