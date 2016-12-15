var Annotation, BoxAnnotation, BoxAnnotationView, PlotWidget, _, properties,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

Annotation = require("./annotation");

PlotWidget = require("../../common/plot_widget");

properties = require("../../common/properties");

BoxAnnotationView = (function(superClass) {
  extend(BoxAnnotationView, superClass);

  function BoxAnnotationView() {
    return BoxAnnotationView.__super__.constructor.apply(this, arguments);
  }

  BoxAnnotationView.prototype.initialize = function(options) {
    BoxAnnotationView.__super__.initialize.call(this, options);
    this.fill_props = new properties.Fill({
      obj: this.model,
      prefix: ''
    });
    this.line_props = new properties.Line({
      obj: this.model,
      prefix: ''
    });
    this.$el.appendTo(this.plot_view.$el.find('div.bk-canvas-overlays'));
    this.$el.addClass('shading');
    return this.$el.hide();
  };

  BoxAnnotationView.prototype.bind_bokeh_events = function() {
    if (this.mget('render_mode') === 'css') {
      return this.listenTo(this.model, 'data_update', this.render);
    } else {
      return this.listenTo(this.model, 'data_update', this.plot_view.request_render);
    }
  };

  BoxAnnotationView.prototype.render = function() {
    var sbottom, sleft, sright, stop;
    if ((this.mget('left') == null) && (this.mget('right') == null) && (this.mget('top') == null) && (this.mget('bottom') == null)) {
      this.$el.hide();
      return null;
    }
    this.frame = this.plot_model.get('frame');
    this.canvas = this.plot_model.get('canvas');
    this.xmapper = this.plot_view.frame.get('x_mappers')[this.mget("x_range_name")];
    this.ymapper = this.plot_view.frame.get('y_mappers')[this.mget("y_range_name")];
    sleft = this.canvas.vx_to_sx(this._calc_dim('left', this.xmapper, this.frame.get('h_range').get('start')));
    sright = this.canvas.vx_to_sx(this._calc_dim('right', this.xmapper, this.frame.get('h_range').get('end')));
    sbottom = this.canvas.vy_to_sy(this._calc_dim('bottom', this.ymapper, this.frame.get('v_range').get('start')));
    stop = this.canvas.vy_to_sy(this._calc_dim('top', this.ymapper, this.frame.get('v_range').get('end')));
    if (this.mget('render_mode') === 'css') {
      return this._css_box(sleft, sright, sbottom, stop);
    } else {
      return this._canvas_box(sleft, sright, sbottom, stop);
    }
  };

  BoxAnnotationView.prototype._css_box = function(sleft, sright, sbottom, stop) {
    var ba, bc, lc, ld, lw, sh, style, sw;
    sw = Math.abs(sright - sleft);
    sh = Math.abs(sbottom - stop);
    lw = this.mget("line_width").value;
    lc = this.mget("line_color").value;
    bc = this.mget("fill_color").value;
    ba = this.mget("fill_alpha").value;
    style = "left:" + sleft + "px; width:" + sw + "px; top:" + stop + "px; height:" + sh + "px; border-width:" + lw + "px; border-color:" + lc + "; background-color:" + bc + "; opacity:" + ba + ";";
    ld = this.mget("line_dash");
    if (_.isArray(ld)) {
      if (ld.length < 2) {
        ld = "solid";
      } else {
        ld = "dashed";
      }
    }
    if (_.isString(ld)) {
      style += " border-style:" + ld + ";";
    }
    this.$el.attr('style', style);
    return this.$el.show();
  };

  BoxAnnotationView.prototype._canvas_box = function(sleft, sright, sbottom, stop) {
    var ctx;
    ctx = this.plot_view.canvas_view.ctx;
    ctx.save();
    ctx.beginPath();
    ctx.rect(sleft, stop, sright - sleft, sbottom - stop);
    this.fill_props.set_value(ctx);
    ctx.fill();
    this.line_props.set_value(ctx);
    ctx.stroke();
    return ctx.restore();
  };

  BoxAnnotationView.prototype._calc_dim = function(dim, mapper, frame_extrema) {
    var vdim;
    if (this.mget(dim) != null) {
      if (this.mget(dim + '_units') === 'data') {
        vdim = mapper.map_to_target(this.mget(dim));
      } else {
        vdim = this.mget(dim);
      }
    } else {
      vdim = frame_extrema;
    }
    return vdim;
  };

  return BoxAnnotationView;

})(PlotWidget);

BoxAnnotation = (function(superClass) {
  extend(BoxAnnotation, superClass);

  function BoxAnnotation() {
    return BoxAnnotation.__super__.constructor.apply(this, arguments);
  }

  BoxAnnotation.prototype.default_view = BoxAnnotationView;

  BoxAnnotation.prototype.type = 'BoxAnnotation';

  BoxAnnotation.prototype.nonserializable_attribute_names = function() {
    return BoxAnnotation.__super__.nonserializable_attribute_names.call(this).concat(['silent_update']);
  };

  BoxAnnotation.prototype.update = function(arg) {
    var bottom, left, right, top;
    left = arg.left, right = arg.right, top = arg.top, bottom = arg.bottom;
    if (this.get('silent_update')) {
      this.attributes['left'] = left;
      this.attributes['right'] = right;
      this.attributes['top'] = top;
      this.attributes['bottom'] = bottom;
    } else {
      this.set({
        left: left,
        right: right,
        top: top,
        bottom: bottom
      });
    }
    return this.trigger('data_update');
  };

  BoxAnnotation.prototype.defaults = function() {
    return _.extend({}, BoxAnnotation.__super__.defaults.call(this), {
      silent_update: false,
      render_mode: "canvas",
      x_range_name: "default",
      y_range_name: "default",
      level: 'annotation',
      left: null,
      right: null,
      top: null,
      bottom: null,
      left_units: 'data',
      right_units: 'data',
      top_units: 'data',
      bottom_units: 'data',
      fill_color: '#fff9ba',
      fill_alpha: 0.4,
      line_color: '#cccccc',
      line_width: 1,
      line_alpha: 0.3,
      line_join: 'miter',
      line_cap: 'butt',
      line_dash: [],
      line_dash_offset: 0
    });
  };

  return BoxAnnotation;

})(Annotation.Model);

module.exports = {
  Model: BoxAnnotation,
  View: BoxAnnotationView
};
