var CategoricalMapper, ContinuumView, Glyph, GlyphView, Model, _, arrayMax, bbox, logger, proj4, properties, rbush, toProjection,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

rbush = require("rbush");

bbox = require("../../common/bbox");

logger = require("../../common/logging").logger;

arrayMax = require("../../common/mathutils").arrayMax;

Model = require("../../model");

ContinuumView = require("../../common/continuum_view");

properties = require("../../common/properties");

CategoricalMapper = require("../mappers/categorical_mapper");

proj4 = require("proj4");

toProjection = proj4.defs('GOOGLE');

GlyphView = (function(superClass) {
  extend(GlyphView, superClass);

  function GlyphView() {
    return GlyphView.__super__.constructor.apply(this, arguments);
  }

  GlyphView.prototype.initialize = function(options) {
    var ctx, func, name, ref, ref1;
    GlyphView.__super__.initialize.call(this, options);
    this.model.glyph_view = this;
    this.renderer = options.renderer;
    if (((ref = this.renderer) != null ? ref.plot_view : void 0) != null) {
      ctx = this.renderer.plot_view.canvas_view.ctx;
      if (ctx.glcanvas != null) {
        this._init_gl(ctx.glcanvas.gl);
      }
    }
    ref1 = properties.factories;
    for (name in ref1) {
      func = ref1[name];
      this[name] = {};
      this[name] = _.extend(this[name], func(this.model));
    }
    this.warned = {};
    return this;
  };

  GlyphView.prototype.render = function(ctx, indices, data) {
    if (this.mget("visible")) {
      ctx.beginPath();
      if (this.glglyph != null) {
        if (this._render_gl(ctx, indices, data)) {
          return;
        }
      }
      return this._render(ctx, indices, data);
    }
  };

  GlyphView.prototype._render_gl = function(ctx, indices, mainglyph) {
    var dx, dy, ref, ref1, trans, wx, wy;
    wx = wy = 1;
    ref = this.renderer.map_to_screen([0 * wx, 1 * wx, 2 * wx], [0 * wy, 1 * wy, 2 * wy]), dx = ref[0], dy = ref[1];
    wx = 100 / Math.min(Math.max(Math.abs(dx[1] - dx[0]), 1e-12), 1e12);
    wy = 100 / Math.min(Math.max(Math.abs(dy[1] - dy[0]), 1e-12), 1e12);
    ref1 = this.renderer.map_to_screen([0 * wx, 1 * wx, 2 * wx], [0 * wy, 1 * wy, 2 * wy]), dx = ref1[0], dy = ref1[1];
    if (Math.abs((dx[1] - dx[0]) - (dx[2] - dx[1])) > 1e-6 || Math.abs((dy[1] - dy[0]) - (dy[2] - dy[1])) > 1e-6) {
      return false;
    }
    trans = {
      width: ctx.glcanvas.width,
      height: ctx.glcanvas.height,
      dx: dx,
      dy: dy,
      sx: (dx[1] - dx[0]) / wx,
      sy: (dy[1] - dy[0]) / wy
    };
    this.glglyph.draw(indices, mainglyph, trans);
    return true;
  };

  GlyphView.prototype.map_data = function() {
    var i, j, k, len, ref, ref1, ref2, ref3, ref4, ref5, ref6, sx, sxname, sy, syname, xname, yname;
    ref = this.model.coords;
    for (j = 0, len = ref.length; j < len; j++) {
      ref1 = ref[j], xname = ref1[0], yname = ref1[1];
      sxname = "s" + xname;
      syname = "s" + yname;
      if (_.isArray((ref2 = this[xname]) != null ? ref2[0] : void 0)) {
        ref3 = [[], []], this[sxname] = ref3[0], this[syname] = ref3[1];
        for (i = k = 0, ref4 = this[xname].length; 0 <= ref4 ? k < ref4 : k > ref4; i = 0 <= ref4 ? ++k : --k) {
          ref5 = this.renderer.map_to_screen(this[xname][i], this[yname][i]), sx = ref5[0], sy = ref5[1];
          this[sxname].push(sx);
          this[syname].push(sy);
        }
      } else {
        ref6 = this.renderer.map_to_screen(this[xname], this[yname]), this[sxname] = ref6[0], this[syname] = ref6[1];
      }
    }
    return this._map_data();
  };

  GlyphView.prototype.project_xy = function(x, y) {
    var i, j, merc_x, merc_x_s, merc_y, merc_y_s, ref, ref1;
    merc_x_s = [];
    merc_y_s = [];
    for (i = j = 0, ref = x.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      ref1 = proj4(toProjection, [x[i], y[i]]), merc_x = ref1[0], merc_y = ref1[1];
      merc_x_s[i] = merc_x;
      merc_y_s[i] = merc_y;
    }
    return [merc_x_s, merc_y_s];
  };

  GlyphView.prototype.project_xsys = function(xs, ys) {
    var i, j, merc_x_s, merc_xs_s, merc_y_s, merc_ys_s, ref, ref1;
    merc_xs_s = [];
    merc_ys_s = [];
    for (i = j = 0, ref = xs.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      ref1 = this.project_xy(xs[i], ys[i]), merc_x_s = ref1[0], merc_y_s = ref1[1];
      merc_xs_s[i] = merc_x_s;
      merc_ys_s[i] = merc_y_s;
    }
    return [merc_xs_s, merc_ys_s];
  };

  GlyphView.prototype.set_data = function(source) {
    var name, prop, ref, ref1, ref2, ref3, ref4, ref5;
    ref = this.coords;
    for (name in ref) {
      prop = ref[name];
      this[name] = prop.array(source);
    }
    if (this.renderer.plot_model.use_map) {
      if (this.x != null) {
        ref1 = this.project_xy(this.x, this.y), this.x = ref1[0], this.y = ref1[1];
      }
      if (this.xs != null) {
        ref2 = this.project_xsys(this.xs, this.ys), this.xs = ref2[0], this.ys = ref2[1];
      }
    }
    ref3 = this.angles;
    for (name in ref3) {
      prop = ref3[name];
      this[name] = prop.array(source);
    }
    ref4 = this.distances;
    for (name in ref4) {
      prop = ref4[name];
      this[name] = prop.array(source);
      this["max_" + name] = arrayMax(this[name]);
    }
    ref5 = this.fields;
    for (name in ref5) {
      prop = ref5[name];
      this[name] = prop.array(source);
    }
    if (this.glglyph != null) {
      this.glglyph.set_data_changed(this.x.length);
    }
    this._set_data();
    return this.index = this._index_data();
  };

  GlyphView.prototype.set_visuals = function(source) {
    var name, prop, ref;
    ref = this.visuals;
    for (name in ref) {
      prop = ref[name];
      prop.warm_cache(source);
    }
    if (this.glglyph != null) {
      return this.glglyph.set_visuals_changed();
    }
  };

  GlyphView.prototype.bounds = function() {
    var bb;
    if (this.index == null) {
      return bbox.empty();
    }
    bb = this.index.data.bbox;
    return this._bounds([[bb[0], bb[2]], [bb[1], bb[3]]]);
  };

  GlyphView.prototype.scx = function(i) {
    return this.sx[i];
  };

  GlyphView.prototype.scy = function(i) {
    return this.sy[i];
  };

  GlyphView.prototype._init_gl = function() {
    return false;
  };

  GlyphView.prototype._set_data = function() {
    return null;
  };

  GlyphView.prototype._map_data = function() {
    return null;
  };

  GlyphView.prototype._mask_data = function(inds) {
    return inds;
  };

  GlyphView.prototype._bounds = function(bds) {
    return bds;
  };

  GlyphView.prototype._xy_index = function() {
    var i, index, j, pts, ref, x, xx, y, yy;
    index = rbush();
    pts = [];
    if (this.renderer.xmapper instanceof CategoricalMapper.Model) {
      xx = this.renderer.xmapper.v_map_to_target(this.x, true);
    } else {
      xx = this.x;
    }
    if (this.renderer.ymapper instanceof CategoricalMapper.Model) {
      yy = this.renderer.ymapper.v_map_to_target(this.y, true);
    } else {
      yy = this.y;
    }
    for (i = j = 0, ref = xx.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      x = xx[i];
      if (isNaN(x) || !isFinite(x)) {
        continue;
      }
      y = yy[i];
      if (isNaN(y) || !isFinite(y)) {
        continue;
      }
      pts.push([
        x, y, x, y, {
          'i': i
        }
      ]);
    }
    index.load(pts);
    return index;
  };

  GlyphView.prototype.sdist = function(mapper, pts, spans, pts_location, dilate) {
    var d, halfspan, i, pt0, pt1, spt0, spt1;
    if (pts_location == null) {
      pts_location = "edge";
    }
    if (dilate == null) {
      dilate = false;
    }
    if (_.isString(pts[0])) {
      pts = mapper.v_map_to_target(pts);
    }
    if (pts_location === 'center') {
      halfspan = (function() {
        var j, len, results;
        results = [];
        for (j = 0, len = spans.length; j < len; j++) {
          d = spans[j];
          results.push(d / 2);
        }
        return results;
      })();
      pt0 = (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = pts.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(pts[i] - halfspan[i]);
        }
        return results;
      })();
      pt1 = (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = pts.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(pts[i] + halfspan[i]);
        }
        return results;
      })();
    } else {
      pt0 = pts;
      pt1 = (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = pt0.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(pt0[i] + spans[i]);
        }
        return results;
      })();
    }
    spt0 = mapper.v_map_to_target(pt0);
    spt1 = mapper.v_map_to_target(pt1);
    if (dilate) {
      return (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = spt0.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(Math.ceil(Math.abs(spt1[i] - spt0[i])));
        }
        return results;
      })();
    } else {
      return (function() {
        var j, ref, results;
        results = [];
        for (i = j = 0, ref = spt0.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
          results.push(Math.abs(spt1[i] - spt0[i]));
        }
        return results;
      })();
    }
  };

  GlyphView.prototype.hit_test = function(geometry) {
    var func, result;
    result = null;
    func = "_hit_" + geometry.type;
    if (this[func] != null) {
      result = this[func](geometry);
    } else if (this.warned[geometry.type] == null) {
      logger.error("'" + geometry.type + "' selection not available for " + this.model.type);
      this.warned[geometry.type] = true;
    }
    return result;
  };

  GlyphView.prototype.get_reference_point = function() {
    var reference_point;
    reference_point = this.mget('reference_point');
    if (_.isNumber(reference_point)) {
      return this.data[reference_point];
    } else {
      return reference_point;
    }
  };

  GlyphView.prototype.draw_legend = function(ctx, x0, x1, y0, y1) {
    return null;
  };

  GlyphView.prototype._generic_line_legend = function(ctx, x0, x1, y0, y1) {
    var ref, reference_point;
    reference_point = (ref = this.get_reference_point()) != null ? ref : 0;
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(x0, (y0 + y1) / 2);
    ctx.lineTo(x1, (y0 + y1) / 2);
    if (this.visuals.line.do_stroke) {
      this.visuals.line.set_vectorize(ctx, reference_point);
      ctx.stroke();
    }
    return ctx.restore();
  };

  GlyphView.prototype._generic_area_legend = function(ctx, x0, x1, y0, y1) {
    var dh, dw, h, indices, ref, reference_point, sx0, sx1, sy0, sy1, w;
    reference_point = (ref = this.get_reference_point()) != null ? ref : 0;
    indices = [reference_point];
    w = Math.abs(x1 - x0);
    dw = w * 0.1;
    h = Math.abs(y1 - y0);
    dh = h * 0.1;
    sx0 = x0 + dw;
    sx1 = x1 - dw;
    sy0 = y0 + dh;
    sy1 = y1 - dh;
    if (this.visuals.fill.do_fill) {
      this.visuals.fill.set_vectorize(ctx, reference_point);
      ctx.fillRect(sx0, sy0, sx1 - sx0, sy1 - sy0);
    }
    if (this.visuals.line.do_stroke) {
      ctx.beginPath();
      ctx.rect(sx0, sy0, sx1 - sx0, sy1 - sy0);
      this.visuals.line.set_vectorize(ctx, reference_point);
      return ctx.stroke();
    }
  };

  return GlyphView;

})(ContinuumView);

Glyph = (function(superClass) {
  extend(Glyph, superClass);

  function Glyph() {
    return Glyph.__super__.constructor.apply(this, arguments);
  }

  Glyph.prototype.visuals = ['line', 'fill'];

  Glyph.prototype.coords = [['x', 'y']];

  Glyph.prototype.distances = [];

  Glyph.prototype.angles = [];

  Glyph.prototype.fields = [];

  Glyph.prototype.fill_defaults = {
    fill_color: 'gray',
    fill_alpha: 1.0
  };

  Glyph.prototype.line_defaults = {
    line_color: 'black',
    line_width: 1,
    line_alpha: 1.0,
    line_join: 'miter',
    line_cap: 'butt',
    line_dash: [],
    line_dash_offset: 0
  };

  Glyph.prototype.text_defaults = {
    text_font: "helvetica",
    text_font_size: "12pt",
    text_font_style: "normal",
    text_color: "#444444",
    text_alpha: 1.0,
    text_align: "left",
    text_baseline: "bottom"
  };

  Glyph.prototype.defaults = function() {
    var defaults, j, len, prop, ref, result;
    result = _.extend({}, Glyph.__super__.defaults.call(this), {
      visible: true
    });
    ref = this.visuals;
    for (j = 0, len = ref.length; j < len; j++) {
      prop = ref[j];
      switch (prop) {
        case 'line':
          defaults = this.line_defaults;
          break;
        case 'fill':
          defaults = this.fill_defaults;
          break;
        case 'text':
          defaults = this.text_defaults;
          break;
        default:
          logger.warn("unknown visual property type '" + prop + "'");
          continue;
      }
      result = _.extend(result, defaults);
    }
    return result;
  };

  return Glyph;

})(Model);

module.exports = {
  Model: Glyph,
  View: GlyphView
};
