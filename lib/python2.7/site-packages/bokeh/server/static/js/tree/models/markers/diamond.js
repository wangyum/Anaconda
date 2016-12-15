var Diamond, DiamondView, Marker, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

DiamondView = (function(superClass) {
  extend(DiamondView, superClass);

  function DiamondView() {
    return DiamondView.__super__.constructor.apply(this, arguments);
  }

  DiamondView.prototype._render = function(ctx, indices, arg) {
    var angle, i, j, len, r, results, size, sx, sy;
    sx = arg.sx, sy = arg.sy, size = arg.size, angle = arg.angle;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sx[i] + sy[i] + size[i] + angle[i])) {
        continue;
      }
      r = size[i] / 2;
      ctx.beginPath();
      ctx.translate(sx[i], sy[i]);
      if (angle[i]) {
        ctx.rotate(angle[i]);
      }
      ctx.moveTo(0, r);
      ctx.lineTo(r / 1.5, 0);
      ctx.lineTo(0, -r);
      ctx.lineTo(-r / 1.5, 0);
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

  return DiamondView;

})(Marker.View);

Diamond = (function(superClass) {
  extend(Diamond, superClass);

  function Diamond() {
    return Diamond.__super__.constructor.apply(this, arguments);
  }

  Diamond.prototype.default_view = DiamondView;

  Diamond.prototype.type = 'Diamond';

  return Diamond;

})(Marker.Model);

module.exports = {
  Model: Diamond,
  View: DiamondView
};
