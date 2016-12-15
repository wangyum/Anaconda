var Annotation, PlotWidget, PolyAnnotation, PolyAnnotationView, _, properties,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Annotation = require("./annotation");

PlotWidget = require("../../common/plot_widget");

properties = require("../../common/properties");

PolyAnnotationView = (function(superClass) {
  extend(PolyAnnotationView, superClass);

  function PolyAnnotationView() {
    return PolyAnnotationView.__super__.constructor.apply(this, arguments);
  }

  PolyAnnotationView.prototype.initialize = function(options) {
    PolyAnnotationView.__super__.initialize.call(this, options);
    this.line = new properties.Line({
      obj: this.model,
      prefix: ""
    });
    return this.fill = new properties.Fill({
      obj: this.model,
      prefix: ""
    });
  };

  PolyAnnotationView.prototype.bind_bokeh_events = function() {
    return this.listenTo(this.model, 'data_update', this.plot_view.request_render);
  };

  PolyAnnotationView.prototype.render = function(ctx) {
    var canvas, i, j, ref, sx, sy, vx, vy, xs, ys;
    xs = this.mget('xs');
    ys = this.mget('ys');
    if (xs.length !== ys.length) {
      return null;
    }
    if (xs.length < 3 || ys.length < 3) {
      return null;
    }
    canvas = this.plot_view.canvas;
    ctx = this.plot_view.canvas_view.ctx;
    for (i = j = 0, ref = xs.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
      if (this.mget('xs_units') === 'screen') {
        vx = xs[i];
      }
      if (this.mget('ys_units') === 'screen') {
        vy = ys[i];
      }
      sx = canvas.vx_to_sx(vx);
      sy = canvas.vy_to_sy(vy);
      if (i === 0) {
        ctx.beginPath();
        ctx.moveTo(sx, sy);
      } else {
        ctx.lineTo(sx, sy);
      }
    }
    ctx.closePath();
    if (this.line.do_stroke) {
      this.line.set_value(ctx);
      ctx.stroke();
    }
    if (this.fill.do_fill) {
      this.fill.set_value(ctx);
      return ctx.fill();
    }
  };

  return PolyAnnotationView;

})(PlotWidget);

PolyAnnotation = (function(superClass) {
  extend(PolyAnnotation, superClass);

  function PolyAnnotation() {
    return PolyAnnotation.__super__.constructor.apply(this, arguments);
  }

  PolyAnnotation.prototype.default_view = PolyAnnotationView;

  PolyAnnotation.prototype.type = "PolyAnnotation";

  PolyAnnotation.prototype.nonserializable_attribute_names = function() {
    return PolyAnnotation.__super__.nonserializable_attribute_names.call(this).concat(['silent_update']);
  };

  PolyAnnotation.prototype.update = function(arg) {
    var xs, ys;
    xs = arg.xs, ys = arg.ys;
    if (this.get('silent_update')) {
      this.attributes['xs'] = xs;
      this.attributes['ys'] = ys;
    } else {
      this.set({
        xs: xs,
        ys: ys
      });
    }
    return this.trigger('data_update');
  };

  PolyAnnotation.prototype.defaults = function() {
    return _.extend({}, PolyAnnotation.__super__.defaults.call(this), {
      silent_update: false,
      plot: null,
      xs: [],
      ys: [],
      xs_units: "data",
      ys_units: "data",
      x_range_name: "default",
      y_range_name: "default",
      level: 'annotation',
      fill_color: "#fff9ba",
      fill_alpha: 0.4,
      line_width: 1,
      line_color: "#cccccc",
      line_alpha: 0.3,
      line_alpha: 0.3,
      line_join: 'miter',
      line_cap: 'butt',
      line_dash: [],
      line_dash_offset: 0
    });
  };

  return PolyAnnotation;

})(Annotation.Model);

module.exports = {
  Model: PolyAnnotation,
  View: PolyAnnotationView
};
