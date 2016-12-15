var CircleX, CircleXView, Marker, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

CircleXView = (function(superClass) {
  extend(CircleXView, superClass);

  function CircleXView() {
    return CircleXView.__super__.constructor.apply(this, arguments);
  }

  CircleXView.prototype._render = function(ctx, indices, arg) {
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
      ctx.arc(0, 0, r, 0, 2 * Math.PI, false);
      if (this.visuals.fill.do_fill) {
        this.visuals.fill.set_vectorize(ctx, i);
        ctx.fill();
      }
      if (this.visuals.line.do_stroke) {
        this.visuals.line.set_vectorize(ctx, i);
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
        ctx.stroke();
      }
      results.push(ctx.translate(-sx[i], -sy[i]));
    }
    return results;
  };

  return CircleXView;

})(Marker.View);

CircleX = (function(superClass) {
  extend(CircleX, superClass);

  function CircleX() {
    return CircleX.__super__.constructor.apply(this, arguments);
  }

  CircleX.prototype.default_view = CircleXView;

  CircleX.prototype.type = 'CircleX';

  return CircleX;

})(Marker.Model);

module.exports = {
  Model: CircleX,
  View: CircleXView
};
