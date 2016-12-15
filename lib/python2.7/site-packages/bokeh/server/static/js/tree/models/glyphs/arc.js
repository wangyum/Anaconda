var Arc, ArcView, Glyph, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Glyph = require("./glyph");

ArcView = (function(superClass) {
  extend(ArcView, superClass);

  function ArcView() {
    return ArcView.__super__.constructor.apply(this, arguments);
  }

  ArcView.prototype._index_data = function() {
    return this._xy_index();
  };

  ArcView.prototype._map_data = function() {
    if (this.distances.radius.units === "data") {
      return this.sradius = this.sdist(this.renderer.xmapper, this.x, this.radius);
    } else {
      return this.sradius = this.radius;
    }
  };

  ArcView.prototype._render = function(ctx, indices, arg) {
    var direction, end_angle, i, j, len, results, sradius, start_angle, sx, sy;
    sx = arg.sx, sy = arg.sy, sradius = arg.sradius, start_angle = arg.start_angle, end_angle = arg.end_angle, direction = arg.direction;
    if (this.visuals.line.do_stroke) {
      results = [];
      for (j = 0, len = indices.length; j < len; j++) {
        i = indices[j];
        if (isNaN(sx[i] + sy[i] + sradius[i] + start_angle[i] + end_angle[i] + direction[i])) {
          continue;
        }
        ctx.beginPath();
        ctx.arc(sx[i], sy[i], sradius[i], start_angle[i], end_angle[i], direction[i]);
        this.visuals.line.set_vectorize(ctx, i);
        results.push(ctx.stroke());
      }
      return results;
    }
  };

  ArcView.prototype.draw_legend = function(ctx, x0, x1, y0, y1) {
    return this._generic_line_legend(ctx, x0, x1, y0, y1);
  };

  return ArcView;

})(Glyph.View);

Arc = (function(superClass) {
  extend(Arc, superClass);

  function Arc() {
    return Arc.__super__.constructor.apply(this, arguments);
  }

  Arc.prototype.default_view = ArcView;

  Arc.prototype.type = 'Arc';

  Arc.prototype.visuals = ['line'];

  Arc.prototype.distances = ['radius'];

  Arc.prototype.angles = ['start_angle', 'end_angle'];

  Arc.prototype.fields = ['direction:direction'];

  Arc.prototype.defaults = function() {
    return _.extend({}, Arc.__super__.defaults.call(this), {
      direction: 'anticlock'
    });
  };

  return Arc;

})(Glyph.Model);

module.exports = {
  Model: Arc,
  View: ArcView
};
