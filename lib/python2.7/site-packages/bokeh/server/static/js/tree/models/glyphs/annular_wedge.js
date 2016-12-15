var AnnularWedge, AnnularWedgeView, Glyph, _, hittest, mathutils,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

mathutils = require("../../common/mathutils");

Glyph = require("./glyph");

hittest = require("../../common/hittest");

AnnularWedgeView = (function(superClass) {
  extend(AnnularWedgeView, superClass);

  function AnnularWedgeView() {
    return AnnularWedgeView.__super__.constructor.apply(this, arguments);
  }

  AnnularWedgeView.prototype._index_data = function() {
    return this._xy_index();
  };

  AnnularWedgeView.prototype._map_data = function() {
    var i, j, ref, results;
    if (this.distances.inner_radius.units === "data") {
      this.sinner_radius = this.sdist(this.renderer.xmapper, this.x, this.inner_radius);
    } else {
      this.sinner_radius = this.inner_radius;
    }
    if (this.distances.outer_radius.units === "data") {
      this.souter_radius = this.sdist(this.renderer.xmapper, this.x, this.outer_radius);
    } else {
      this.souter_radius = this.outer_radius;
    }
    this.angle = new Float32Array(this.start_angle.length);
    results = [];
    for (i = j = 0, ref = this.start_angle.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      results.push(this.angle[i] = this.end_angle[i] - this.start_angle[i]);
    }
    return results;
  };

  AnnularWedgeView.prototype._render = function(ctx, indices, arg) {
    var angle, direction, i, j, len, results, sinner_radius, souter_radius, start_angle, sx, sy;
    sx = arg.sx, sy = arg.sy, start_angle = arg.start_angle, angle = arg.angle, sinner_radius = arg.sinner_radius, souter_radius = arg.souter_radius, direction = arg.direction;
    results = [];
    for (j = 0, len = indices.length; j < len; j++) {
      i = indices[j];
      if (isNaN(sx[i] + sy[i] + sinner_radius[i] + souter_radius[i] + start_angle[i] + angle[i] + direction[i])) {
        continue;
      }
      ctx.translate(sx[i], sy[i]);
      ctx.rotate(this.start_angle[i]);
      ctx.moveTo(souter_radius[i], 0);
      ctx.beginPath();
      ctx.arc(0, 0, souter_radius[i], 0, angle[i], direction[i]);
      ctx.rotate(this.angle[i]);
      ctx.lineTo(sinner_radius[i], 0);
      ctx.arc(0, 0, sinner_radius[i], 0, -angle[i], !direction[i]);
      ctx.closePath();
      ctx.rotate(-angle[i] - start_angle[i]);
      ctx.translate(-sx[i], -sy[i]);
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

  AnnularWedgeView.prototype._hit_point = function(geometry) {
    var angle, candidates, dist, hits, i, ir2, j, k, len, len1, or2, pt, ref, ref1, ref2, ref3, ref4, result, sx, sx0, sx1, sy, sy0, sy1, vx, vx0, vx1, vy, vy0, vy1, x, x0, x1, y, y0, y1;
    ref = [geometry.vx, geometry.vy], vx = ref[0], vy = ref[1];
    x = this.renderer.xmapper.map_from_target(vx, true);
    y = this.renderer.ymapper.map_from_target(vy, true);
    if (this.distances.outer_radius.units === "data") {
      x0 = x - this.max_outer_radius;
      x1 = x + this.max_outer_radius;
      y0 = y - this.max_outer_radius;
      y1 = y + this.max_outer_radius;
    } else {
      vx0 = vx - this.max_outer_radius;
      vx1 = vx + this.max_outer_radius;
      ref1 = this.renderer.xmapper.v_map_from_target([vx0, vx1], true), x0 = ref1[0], x1 = ref1[1];
      vy0 = vy - this.max_outer_radius;
      vy1 = vy + this.max_outer_radius;
      ref2 = this.renderer.ymapper.v_map_from_target([vy0, vy1], true), y0 = ref2[0], y1 = ref2[1];
    }
    candidates = [];
    ref3 = (function() {
      var k, len, ref3, results;
      ref3 = this.index.search([x0, y0, x1, y1]);
      results = [];
      for (k = 0, len = ref3.length; k < len; k++) {
        pt = ref3[k];
        results.push(pt[4].i);
      }
      return results;
    }).call(this);
    for (j = 0, len = ref3.length; j < len; j++) {
      i = ref3[j];
      or2 = Math.pow(this.souter_radius[i], 2);
      ir2 = Math.pow(this.sinner_radius[i], 2);
      sx0 = this.renderer.xmapper.map_to_target(x, true);
      sx1 = this.renderer.xmapper.map_to_target(this.x[i], true);
      sy0 = this.renderer.ymapper.map_to_target(y, true);
      sy1 = this.renderer.ymapper.map_to_target(this.y[i], true);
      dist = Math.pow(sx0 - sx1, 2) + Math.pow(sy0 - sy1, 2);
      if (dist <= or2 && dist >= ir2) {
        candidates.push([i, dist]);
      }
    }
    hits = [];
    for (k = 0, len1 = candidates.length; k < len1; k++) {
      ref4 = candidates[k], i = ref4[0], dist = ref4[1];
      sx = this.renderer.plot_view.canvas.vx_to_sx(vx);
      sy = this.renderer.plot_view.canvas.vy_to_sy(vy);
      angle = Math.atan2(sy - this.sy[i], sx - this.sx[i]);
      if (mathutils.angle_between(-angle, -this.start_angle[i], -this.end_angle[i], this.direction[i])) {
        hits.push([i, dist]);
      }
    }
    result = hittest.create_hit_test_result();
    result['1d'].indices = _.chain(hits).sortBy(function(elt) {
      return elt[1];
    }).map(function(elt) {
      return elt[0];
    }).value();
    return result;
  };

  AnnularWedgeView.prototype.draw_legend = function(ctx, x0, x1, y0, y1) {
    return this._generic_area_legend(ctx, x0, x1, y0, y1);
  };

  return AnnularWedgeView;

})(Glyph.View);

AnnularWedge = (function(superClass) {
  extend(AnnularWedge, superClass);

  function AnnularWedge() {
    return AnnularWedge.__super__.constructor.apply(this, arguments);
  }

  AnnularWedge.prototype.default_view = AnnularWedgeView;

  AnnularWedge.prototype.type = 'AnnularWedge';

  AnnularWedge.prototype.distances = ['inner_radius', 'outer_radius'];

  AnnularWedge.prototype.angles = ['start_angle', 'end_angle'];

  AnnularWedge.prototype.fields = ['direction:direction'];

  AnnularWedge.prototype.defaults = function() {
    return _.extend({}, AnnularWedge.__super__.defaults.call(this), {
      direction: 'anticlock'
    });
  };

  return AnnularWedge;

})(Glyph.Model);

module.exports = {
  Model: AnnularWedge,
  View: AnnularWedgeView
};
