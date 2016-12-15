var Annotation, Legend, LegendView, PlotWidget, _, properties, textutils,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Annotation = require("./annotation");

PlotWidget = require("../../common/plot_widget");

properties = require("../../common/properties");

textutils = require("../../common/textutils");

LegendView = (function(superClass) {
  extend(LegendView, superClass);

  function LegendView() {
    return LegendView.__super__.constructor.apply(this, arguments);
  }

  LegendView.prototype.initialize = function(options) {
    LegendView.__super__.initialize.call(this, options);
    this.label_props = new properties.Text({
      obj: this.model,
      prefix: 'label_'
    });
    this.border_props = new properties.Line({
      obj: this.model,
      prefix: 'border_'
    });
    this.background_props = new properties.Fill({
      obj: this.model,
      prefix: 'background_'
    });
    this.need_calc_dims = true;
    return this.listenTo(this.plot_model.solver, 'layout_update', function() {
      return this.need_calc_dims = true;
    });
  };

  LegendView.prototype.calc_dims = function(options) {
    var ctx, glyphs, h_range, label_height, label_width, legend_name, legend_names, legend_padding, legend_spacing, location, text_width, text_widths, v_range, x, y;
    legend_names = (function() {
      var i, len, ref, ref1, results;
      ref = this.mget("legends");
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        ref1 = ref[i], legend_name = ref1[0], glyphs = ref1[1];
        results.push(legend_name);
      }
      return results;
    }).call(this);
    label_height = this.mget('label_height');
    this.glyph_height = this.mget('glyph_height');
    label_width = this.mget('label_width');
    this.glyph_width = this.mget('glyph_width');
    legend_spacing = this.mget('legend_spacing');
    this.label_height = _.max([textutils.getTextHeight(this.label_props.font_value()), label_height, this.glyph_height]);
    this.legend_height = this.label_height;
    this.legend_height = legend_names.length * this.legend_height + (1 + legend_names.length) * legend_spacing;
    ctx = this.plot_view.canvas_view.ctx;
    ctx.save();
    this.label_props.set_value(ctx);
    text_widths = _.map(legend_names, function(txt) {
      return ctx.measureText(txt).width;
    });
    ctx.restore();
    text_width = _.max(text_widths);
    this.label_width = _.max([text_width, label_width]);
    this.legend_width = this.label_width + this.glyph_width + 3 * legend_spacing;
    location = this.mget('location');
    legend_padding = this.mget('legend_padding');
    h_range = this.plot_view.frame.get('h_range');
    v_range = this.plot_view.frame.get('v_range');
    if (_.isString(location)) {
      switch (location) {
        case 'top_left':
          x = h_range.get('start') + legend_padding;
          y = v_range.get('end') - legend_padding;
          break;
        case 'top_center':
          x = (h_range.get('end') + h_range.get('start')) / 2 - this.legend_width / 2;
          y = v_range.get('end') - legend_padding;
          break;
        case 'top_right':
          x = h_range.get('end') - legend_padding - this.legend_width;
          y = v_range.get('end') - legend_padding;
          break;
        case 'right_center':
          x = h_range.get('end') - legend_padding - this.legend_width;
          y = (v_range.get('end') + v_range.get('start')) / 2 + this.legend_height / 2;
          break;
        case 'bottom_right':
          x = h_range.get('end') - legend_padding - this.legend_width;
          y = v_range.get('start') + legend_padding + this.legend_height;
          break;
        case 'bottom_center':
          x = (h_range.get('end') + h_range.get('start')) / 2 - this.legend_width / 2;
          y = v_range.get('start') + legend_padding + this.legend_height;
          break;
        case 'bottom_left':
          x = h_range.get('start') + legend_padding;
          y = v_range.get('start') + legend_padding + this.legend_height;
          break;
        case 'left_center':
          x = h_range.get('start') + legend_padding;
          y = (v_range.get('end') + v_range.get('start')) / 2 + this.legend_height / 2;
          break;
        case 'center':
          x = (h_range.get('end') + h_range.get('start')) / 2 - this.legend_width / 2;
          y = (v_range.get('end') + v_range.get('start')) / 2 + this.legend_height / 2;
      }
    } else if (_.isArray(location) && location.length === 2) {
      x = location[0], y = location[1];
    }
    x = this.plot_view.canvas.vx_to_sx(x);
    y = this.plot_view.canvas.vy_to_sy(y);
    return this.box_coords = [x, y];
  };

  LegendView.prototype.render = function() {
    var ctx, glyphs, i, idx, j, legend_name, legend_spacing, len, len1, ref, ref1, ref2, renderer, view, x, x1, x2, y, y1, y2, yoffset, yspacing;
    if (this.need_calc_dims) {
      this.calc_dims();
      this.need_calc_dims = false;
    }
    ctx = this.plot_view.canvas_view.ctx;
    ctx.save();
    ctx.beginPath();
    ctx.rect(this.box_coords[0], this.box_coords[1], this.legend_width, this.legend_height);
    this.background_props.set_value(ctx);
    ctx.fill();
    if (this.border_props.do_stroke) {
      this.border_props.set_value(ctx);
      ctx.stroke();
    }
    legend_spacing = this.mget('legend_spacing');
    ref = this.mget("legends");
    for (idx = i = 0, len = ref.length; i < len; idx = ++i) {
      ref1 = ref[idx], legend_name = ref1[0], glyphs = ref1[1];
      yoffset = idx * this.label_height;
      yspacing = (1 + idx) * legend_spacing;
      y = this.box_coords[1] + this.label_height / 2.0 + yoffset + yspacing;
      x = this.box_coords[0] + legend_spacing;
      x1 = this.box_coords[0] + 2 * legend_spacing + this.label_width;
      x2 = x1 + this.glyph_width;
      y1 = this.box_coords[1] + yoffset + yspacing;
      y2 = y1 + this.glyph_height;
      this.label_props.set_value(ctx);
      ctx.fillText(legend_name, x, y);
      ref2 = this.model.resolve_ref(glyphs);
      for (j = 0, len1 = ref2.length; j < len1; j++) {
        renderer = ref2[j];
        view = this.plot_view.renderers[renderer.id];
        view.draw_legend(ctx, x1, x2, y1, y2);
      }
    }
    return ctx.restore();
  };

  return LegendView;

})(PlotWidget);

Legend = (function(superClass) {
  extend(Legend, superClass);

  function Legend() {
    return Legend.__super__.constructor.apply(this, arguments);
  }

  Legend.prototype.default_view = LegendView;

  Legend.prototype.type = 'Legend';

  Legend.prototype.defaults = function() {
    return _.extend({}, Legend.__super__.defaults.call(this), {
      legends: [],
      level: "annotation",
      border_line_color: 'black',
      border_line_width: 1,
      border_line_alpha: 1.0,
      border_line_join: 'miter',
      border_line_cap: 'butt',
      border_line_dash: [],
      border_line_dash_offset: 0,
      background_fill_color: "#ffffff",
      background_fill_alpha: 1.0,
      label_standoff: 15,
      label_text_font: "helvetica",
      label_text_font_size: "10pt",
      label_text_font_style: "normal",
      label_text_color: "#444444",
      label_text_alpha: 1.0,
      label_text_align: "left",
      label_text_baseline: "middle",
      glyph_height: 20,
      glyph_width: 20,
      label_height: 20,
      label_width: 50,
      legend_padding: 10,
      legend_spacing: 3,
      location: 'top_right'
    });
  };

  return Legend;

})(Annotation.Model);

module.exports = {
  Model: Legend,
  View: LegendView
};
