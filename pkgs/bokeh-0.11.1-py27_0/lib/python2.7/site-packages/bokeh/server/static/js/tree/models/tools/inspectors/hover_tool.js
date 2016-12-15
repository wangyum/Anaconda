var $, HoverTool, HoverToolView, InspectTool, Tooltip, Util, _, _color_to_hex, hittest, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

logger = require("../../../common/logging").logger;

Tooltip = require("../../annotations/tooltip");

Util = require("../../../util/util");

InspectTool = require("./inspect_tool");

hittest = require("../../../common/hittest");

_color_to_hex = function(color) {
  var blue, digits, green, red, rgb;
  if (color.substr(0, 1) === '#') {
    return color;
  }
  digits = /(.*?)rgb\((\d+), (\d+), (\d+)\)/.exec(color);
  red = parseInt(digits[2]);
  green = parseInt(digits[3]);
  blue = parseInt(digits[4]);
  rgb = blue | (green << 8) | (red << 16);
  return digits[1] + '#' + rgb.toString(16);
};

HoverToolView = (function(superClass) {
  extend(HoverToolView, superClass);

  function HoverToolView() {
    return HoverToolView.__super__.constructor.apply(this, arguments);
  }

  HoverToolView.prototype.bind_bokeh_events = function() {
    var j, len, r, ref;
    ref = this.mget('computed_renderers');
    for (j = 0, len = ref.length; j < len; j++) {
      r = ref[j];
      this.listenTo(r.get('data_source'), 'inspect', this._update);
    }
    return this.plot_view.canvas_view.canvas_wrapper.css('cursor', 'crosshair');
  };

  HoverToolView.prototype._move = function(e) {
    var canvas, ref, rid, tt, vx, vy;
    if (!this.mget('active')) {
      return;
    }
    canvas = this.plot_view.canvas;
    vx = canvas.sx_to_vx(e.bokeh.sx);
    vy = canvas.sy_to_vy(e.bokeh.sy);
    if (!this.plot_view.frame.contains(vx, vy)) {
      ref = this.mget('ttmodels');
      for (rid in ref) {
        tt = ref[rid];
        tt.clear();
      }
      return;
    }
    return this._inspect(vx, vy);
  };

  HoverToolView.prototype._move_exit = function() {
    var ref, results, rid, tt;
    ref = this.mget('ttmodels');
    results = [];
    for (rid in ref) {
      tt = ref[rid];
      results.push(tt.clear());
    }
    return results;
  };

  HoverToolView.prototype._inspect = function(vx, vy, e) {
    var geometry, hovered_indexes, hovered_renderers, j, len, r, ref, sm;
    geometry = {
      type: 'point',
      vx: vx,
      vy: vy
    };
    if (this.mget('mode') === 'mouse') {
      geometry['type'] = 'point';
    } else {
      geometry['type'] = 'span';
      if (this.mget('mode') === 'vline') {
        geometry.direction = 'h';
      } else {
        geometry.direction = 'v';
      }
    }
    hovered_indexes = [];
    hovered_renderers = [];
    ref = this.mget('computed_renderers');
    for (j = 0, len = ref.length; j < len; j++) {
      r = ref[j];
      sm = r.get('data_source').get('selection_manager');
      sm.inspect(this, this.plot_view.renderers[r.id], geometry, {
        "geometry": geometry
      });
    }
    if (this.mget('callback') != null) {
      this._emit_callback(geometry);
    }
  };

  HoverToolView.prototype._update = function(indices, tool, renderer, ds, arg) {
    var canvas, d1x, d1y, d2x, d2y, data_x, data_y, dist1, dist2, frame, geometry, i, i1d, i2d, j, k, len, len1, ref, ref1, ref10, ref2, ref3, ref4, ref5, ref6, ref7, ref8, ref9, rx, ry, sdatax, sdatay, sx, sy, tooltip, vars, vx, vy, x, xmapper, y, ymapper;
    geometry = arg.geometry;
    tooltip = (ref = this.mget('ttmodels')[renderer.model.id]) != null ? ref : null;
    if (tooltip == null) {
      return;
    }
    tooltip.clear();
    ref1 = [indices['1d'].indices, indices['2d'].indices], i1d = ref1[0], i2d = ref1[1];
    if (indices['0d'].glyph === null && i1d.length === 0 && i2d.length === 0) {
      return;
    }
    vx = geometry.vx;
    vy = geometry.vy;
    canvas = this.plot_model.get('canvas');
    frame = this.plot_model.get('frame');
    sx = canvas.vx_to_sx(vx);
    sy = canvas.vy_to_sy(vy);
    xmapper = frame.get('x_mappers')[renderer.mget('x_range_name')];
    ymapper = frame.get('y_mappers')[renderer.mget('y_range_name')];
    x = xmapper.map_from_target(vx);
    y = ymapper.map_from_target(vy);
    ref2 = indices['0d'].indices;
    for (j = 0, len = ref2.length; j < len; j++) {
      i = ref2[j];
      data_x = renderer.glyph.x[i + 1];
      data_y = renderer.glyph.y[i + 1];
      if (this.mget('line_policy') === "interp") {
        ref3 = renderer.glyph.get_interpolation_hit(i, geometry), data_x = ref3[0], data_y = ref3[1];
        rx = xmapper.map_to_target(data_x);
        ry = ymapper.map_to_target(data_y);
      } else if (this.mget('line_policy') === "prev") {
        rx = canvas.sx_to_vx(renderer.glyph.sx[i]);
        ry = canvas.sy_to_vy(renderer.glyph.sy[i]);
      } else if (this.mget('line_policy') === "next") {
        rx = canvas.sx_to_vx(renderer.glyph.sx[i + 1]);
        ry = canvas.sy_to_vy(renderer.glyph.sy[i + 1]);
      } else if (this.mget('line_policy') === "nearest") {
        d1x = renderer.glyph.sx[i];
        d1y = renderer.glyph.sy[i];
        dist1 = hittest.dist_2_pts(d1x, d1y, sx, sy);
        d2x = renderer.glyph.sx[i + 1];
        d2y = renderer.glyph.sy[i + 1];
        dist2 = hittest.dist_2_pts(d2x, d2y, sx, sy);
        if (dist1 < dist2) {
          ref4 = [d1x, d1y], sdatax = ref4[0], sdatay = ref4[1];
        } else {
          ref5 = [d2x, d2y], sdatax = ref5[0], sdatay = ref5[1];
          i = i + 1;
        }
        data_x = renderer.glyph.x[i];
        data_y = renderer.glyph.y[i];
        rx = canvas.sx_to_vx(sdatax);
        ry = canvas.sy_to_vy(sdatay);
      } else {
        ref6 = [vx, vy], rx = ref6[0], ry = ref6[1];
      }
      vars = {
        index: i,
        x: x,
        y: y,
        vx: vx,
        vy: vy,
        sx: sx,
        sy: sy,
        data_x: data_x,
        data_y: data_y,
        rx: rx,
        ry: ry
      };
      tooltip.add(rx, ry, this._render_tooltips(ds, i, vars));
    }
    ref7 = indices['1d'].indices;
    for (k = 0, len1 = ref7.length; k < len1; k++) {
      i = ref7[k];
      data_x = (ref8 = renderer.glyph.x) != null ? ref8[i] : void 0;
      data_y = (ref9 = renderer.glyph.y) != null ? ref9[i] : void 0;
      if (this.mget('point_policy') === 'snap_to_data') {
        rx = canvas.sx_to_vx(renderer.glyph.scx(i, sx, sy));
        ry = canvas.sy_to_vy(renderer.glyph.scy(i, sx, sy));
      } else {
        ref10 = [vx, vy], rx = ref10[0], ry = ref10[1];
      }
      vars = {
        index: i,
        x: x,
        y: y,
        vx: vx,
        vy: vy,
        sx: sx,
        sy: sy,
        data_x: data_x,
        data_y: data_y
      };
      tooltip.add(rx, ry, this._render_tooltips(ds, i, vars));
    }
    return null;
  };

  HoverToolView.prototype._emit_callback = function(geometry) {
    var canvas, frame, indices, r, xmapper, ymapper;
    r = this.mget('computed_renderers')[0];
    indices = this.plot_view.renderers[r.id].hit_test(geometry);
    canvas = this.plot_model.get('canvas');
    frame = this.plot_model.get('frame');
    geometry['sx'] = canvas.vx_to_sx(geometry.vx);
    geometry['sy'] = canvas.vy_to_sy(geometry.vy);
    xmapper = frame.get('x_mappers')[r.get('x_range_name')];
    ymapper = frame.get('y_mappers')[r.get('y_range_name')];
    geometry['x'] = xmapper.map_from_target(geometry.vx);
    geometry['y'] = ymapper.map_from_target(geometry.vy);
    this.mget('callback').execute(this.model, {
      index: indices,
      geometry: geometry
    });
  };

  HoverToolView.prototype._render_tooltips = function(ds, i, vars) {
    var colname, color, column, hex, j, label, len, match, opts, ref, ref1, row, span, swatch, table, td, tooltips, value;
    tooltips = this.mget("tooltips");
    if (_.isString(tooltips)) {
      return $('<div>').html(Util.replace_placeholders(tooltips, ds, i, vars));
    } else {
      table = $('<table></table>');
      for (j = 0, len = tooltips.length; j < len; j++) {
        ref = tooltips[j], label = ref[0], value = ref[1];
        row = $("<tr></tr>");
        row.append($("<td class='bk-tooltip-row-label'>").text(label + ": "));
        td = $("<td class='bk-tooltip-row-value'></td>");
        if (value.indexOf("$color") >= 0) {
          ref1 = value.match(/\$color(\[.*\])?:(\w*)/), match = ref1[0], opts = ref1[1], colname = ref1[2];
          column = ds.get_column(colname);
          if (column == null) {
            span = $("<span>").text(colname + " unknown");
            td.append(span);
            continue;
          }
          hex = (opts != null ? opts.indexOf("hex") : void 0) >= 0;
          swatch = (opts != null ? opts.indexOf("swatch") : void 0) >= 0;
          color = column[i];
          if (color == null) {
            span = $("<span>(null)</span>");
            td.append(span);
            continue;
          }
          if (hex) {
            color = _color_to_hex(color);
          }
          span = $("<span>").text(color);
          td.append(span);
          if (swatch) {
            span = $("<span class='bk-tooltip-color-block'> </span>");
            span.css({
              backgroundColor: color
            });
          }
          td.append(span);
        } else {
          value = value.replace("$~", "$data_");
          value = Util.replace_placeholders(value, ds, i, vars);
          td.append($('<span>').html(value));
        }
        row.append(td);
        table.append(row);
      }
      return table;
    }
  };

  return HoverToolView;

})(InspectTool.View);

HoverTool = (function(superClass) {
  extend(HoverTool, superClass);

  function HoverTool() {
    return HoverTool.__super__.constructor.apply(this, arguments);
  }

  HoverTool.prototype.default_view = HoverToolView;

  HoverTool.prototype.type = "HoverTool";

  HoverTool.prototype.tool_name = "Hover Tool";

  HoverTool.prototype.icon = "bk-tool-icon-hover";

  HoverTool.prototype.nonserializable_attribute_names = function() {
    return HoverTool.__super__.nonserializable_attribute_names.call(this).concat(['ttmodels', 'computed_renderers']);
  };

  HoverTool.prototype.initialize = function(attrs, options) {
    return HoverTool.__super__.initialize.call(this, attrs, options);
  };

  HoverTool.prototype.initialize = function(attrs, options) {
    var all_renderers, j, k, len, len1, names, r, ref, renderers, tooltip, tooltips, ttmodels;
    HoverTool.__super__.initialize.call(this, attrs, options);
    names = this.get('names');
    renderers = this.get('renderers');
    if (renderers.length === 0) {
      all_renderers = this.get('plot').get('renderers');
      renderers = (function() {
        var j, len, results;
        results = [];
        for (j = 0, len = all_renderers.length; j < len; j++) {
          r = all_renderers[j];
          if (r.type === "GlyphRenderer") {
            results.push(r);
          }
        }
        return results;
      })();
    }
    if (names.length > 0) {
      renderers = (function() {
        var j, len, results;
        results = [];
        for (j = 0, len = renderers.length; j < len; j++) {
          r = renderers[j];
          if (names.indexOf(r.get('name')) >= 0) {
            results.push(r);
          }
        }
        return results;
      })();
    }
    this.set('computed_renderers', renderers);
    logger.debug("setting " + renderers.length + " computed renderers for " + this.type + " " + this.id);
    for (j = 0, len = renderers.length; j < len; j++) {
      r = renderers[j];
      logger.debug("  - " + r.type + " " + r.id);
    }
    ttmodels = {};
    renderers = this.get('plot').get('renderers');
    tooltips = this.get("tooltips");
    if (tooltips != null) {
      ref = this.get('computed_renderers');
      for (k = 0, len1 = ref.length; k < len1; k++) {
        r = ref[k];
        tooltip = new Tooltip.Model();
        tooltip.set("custom", _.isString(tooltips));
        ttmodels[r.id] = tooltip;
        renderers.push(tooltip);
      }
    }
    this.set('ttmodels', ttmodels);
    this.get('plot').set('renderers', renderers);
  };

  HoverTool.prototype.defaults = function() {
    return _.extend({}, HoverTool.__super__.defaults.call(this), {
      tooltips: [["index", "$index"], ["data (x, y)", "($x, $y)"], ["canvas (x, y)", "($sx, $sy)"]],
      renderers: [],
      names: [],
      mode: 'mouse',
      point_policy: "snap_to_data",
      line_policy: "prev",
      callback: null
    });
  };

  return HoverTool;

})(InspectTool.Model);

module.exports = {
  Model: HoverTool,
  View: HoverToolView
};
