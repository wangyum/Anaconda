var Asterisk, AsteriskView, Marker, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Marker = require("./marker");

AsteriskView = (function(superClass) {
  extend(AsteriskView, superClass);

  function AsteriskView() {
    return AsteriskView.__super__.constructor.apply(this, arguments);
  }

  AsteriskView.prototype._render = function(ctx, indices, arg) {
    var angle, i, j, len, r, r2, results, size, sx, sy;
    sx = arg.sx, sy = arg.sy, size = arg.size, angle = arg.angle;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sx[i] + sy[i] + size[i] + angle[i])) {
        continue;
      }
      r = size[i] / 2;
      r2 = r * 0.65;
      ctx.beginPath();
      ctx.translate(sx[i], sy[i]);
      if (angle[i]) {
        ctx.rotate(angle[i]);
      }
      ctx.moveTo(0, r);
      ctx.lineTo(0, -r);
      ctx.moveTo(-r, 0);
      ctx.lineTo(r, 0);
      ctx.moveTo(-r2, r2);
      ctx.lineTo(r2, -r2);
      ctx.moveTo(-r2, -r2);
      ctx.lineTo(r2, r2);
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

  return AsteriskView;

})(Marker.View);

Asterisk = (function(superClass) {
  extend(Asterisk, superClass);

  function Asterisk() {
    return Asterisk.__super__.constructor.apply(this, arguments);
  }

  Asterisk.prototype.default_view = AsteriskView;

  Asterisk.prototype.type = 'Asterisk';

  Asterisk.prototype.props = ['line'];

  return Asterisk;

})(Marker.Model);

module.exports = {
  Model: Asterisk,
  View: AsteriskView
};
