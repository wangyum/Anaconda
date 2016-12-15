var Glyph, Quad, QuadView, _, hittest, rbush,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

rbush = require("rbush");

Glyph = require("./glyph");

hittest = require("../../common/hittest");

QuadView = (function(superClass) {
  extend(QuadView, superClass);

  function QuadView() {
    return QuadView.__super__.constructor.apply(this, arguments);
  }

  QuadView.prototype._index_data = function() {
    var i, index, j, pts, ref;
    index = rbush();
    pts = [];
    for (i = j = 0, ref = this.left.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      if (!isNaN(this.left[i] + this.right[i] + this.top[i] + this.bottom[i])) {
        pts.push([
          this.left[i], this.bottom[i], this.right[i], this.top[i], {
            'i': i
          }
        ]);
      }
    }
    index.load(pts);
    return index;
  };

  QuadView.prototype._render = function(ctx, indices, arg) {
    var i, j, len, results, sbottom, sleft, sright, stop;
    sleft = arg.sleft, sright = arg.sright, stop = arg.stop, sbottom = arg.sbottom;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sleft[i] + stop[i] + sright[i] + sbottom[i])) {
        continue;
      }
      if (this.visuals.fill.do_fill) {
        this.visuals.fill.set_vectorize(ctx, i);
        ctx.fillRect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
      }
      if (this.visuals.line.do_stroke) {
        ctx.beginPath();
        ctx.rect(sleft[i], stop[i], sright[i] - sleft[i], sbottom[i] - stop[i]);
        this.visuals.line.set_vectorize(ctx, i);
        results.push(ctx.stroke());
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  QuadView.prototype._hit_point = function(geometry) {
    var hits, ref, result, vx, vy, x, y;
    ref = [geometry.vx, geometry.vy], vx = ref[0], vy = ref[1];
    x = this.renderer.xmapper.map_from_target(vx, true);
    y = this.renderer.ymapper.map_from_target(vy, true);
    hits = (function() {
      var j, len, ref1, results;
      ref1 = this.index.search([x, y, x, y]);
      results = [];
      for (j = 0, len = ref1.length; j < len; j++) {
        x = ref1[j];
        results.push(x[4].i);
      }
      return results;
    }).call(this);
    result = hittest.create_hit_test_result();
    result['1d'].indices = hits;
    return result;
  };

  QuadView.prototype.scx = function(i) {
    return (this.sleft[i] + this.sright[i]) / 2;
  };

  QuadView.prototype.scy = function(i) {
    return (this.stop[i] + this.sbottom[i]) / 2;
  };

  QuadView.prototype.draw_legend = function(ctx, x0, x1, y0, y1) {
    return this._generic_area_legend(ctx, x0, x1, y0, y1);
  };

  return QuadView;

})(Glyph.View);

Quad = (function(superClass) {
  extend(Quad, superClass);

  function Quad() {
    return Quad.__super__.constructor.apply(this, arguments);
  }

  Quad.prototype.default_view = QuadView;

  Quad.prototype.type = 'Quad';

  Quad.prototype.coords = [['right', 'bottom'], ['left', 'top']];

  return Quad;

})(Glyph.Model);

module.exports = {
  Model: Quad,
  View: QuadView
};
