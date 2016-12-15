var Marker, X, XView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

XView = (function(superClass) {
  extend(XView, superClass);

  function XView() {
    return XView.__super__.constructor.apply(this, arguments);
  }

  XView.prototype._render = function(ctx, indices, arg) {
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
      ctx.moveTo(-r, r);
      ctx.lineTo(r, -r);
      ctx.moveTo(-r, -r);
      ctx.lineTo(r, r);
      if (angle[i]) {
        ctx.rotate(-angle[i]);
      }
      if (this.visuals.line.do_stroke) {
        this.visuals.line.set_vectorize(ctx, i);
        ctx.stroke();
      }
      results.push(ctx.translate(-sx[i], -sy[i]));
    }
    return results;
  };

  return XView;

})(Marker.View);

X = (function(superClass) {
  extend(X, superClass);

  function X() {
    return X.__super__.constructor.apply(this, arguments);
  }

  X.prototype.default_view = XView;

  X.prototype.type = 'X';

  X.prototype.props = ['line'];

  return X;

})(Marker.Model);

module.exports = {
  Model: X,
  View: XView
};
