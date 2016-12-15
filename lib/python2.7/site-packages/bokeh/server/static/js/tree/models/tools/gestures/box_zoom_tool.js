var BoxAnnotation, BoxZoomTool, BoxZoomToolView, GestureTool, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

GestureTool = require("./gesture_tool");

BoxAnnotation = require("../../annotations/box_annotation");

BoxZoomToolView = (function(superClass) {
  extend(BoxZoomToolView, superClass);

  function BoxZoomToolView() {
    return BoxZoomToolView.__super__.constructor.apply(this, arguments);
  }

  BoxZoomToolView.prototype._pan_start = function(e) {
    var canvas;
    canvas = this.plot_view.canvas;
    this._baseboint = [canvas.sx_to_vx(e.bokeh.sx), canvas.sy_to_vy(e.bokeh.sy)];
    return null;
  };

  BoxZoomToolView.prototype._pan = function(e) {
    var canvas, curpoint, dims, frame, ref, vxlim, vylim;
    canvas = this.plot_view.canvas;
    curpoint = [canvas.sx_to_vx(e.bokeh.sx), canvas.sy_to_vy(e.bokeh.sy)];
    frame = this.plot_model.get('frame');
    dims = this.mget('dimensions');
    ref = this.model._get_dim_limits(this._baseboint, curpoint, frame, dims), vxlim = ref[0], vylim = ref[1];
    this.mget('overlay').update({
      left: vxlim[0],
      right: vxlim[1],
      top: vylim[1],
      bottom: vylim[0]
    });
    return null;
  };

  BoxZoomToolView.prototype._pan_end = function(e) {
    var canvas, curpoint, dims, frame, ref, vxlim, vylim;
    canvas = this.plot_view.canvas;
    curpoint = [canvas.sx_to_vx(e.bokeh.sx), canvas.sy_to_vy(e.bokeh.sy)];
    frame = this.plot_model.get('frame');
    dims = this.mget('dimensions');
    ref = this.model._get_dim_limits(this._baseboint, curpoint, frame, dims), vxlim = ref[0], vylim = ref[1];
    this._update(vxlim, vylim);
    this.mget('overlay').update({
      left: null,
      right: null,
      top: null,
      bottom: null
    });
    this._baseboint = null;
    return null;
  };

  BoxZoomToolView.prototype._update = function(vxlim, vylim) {
    var end, mapper, name, ref, ref1, ref2, ref3, start, xrs, yrs, zoom_info;
    if (Math.abs(vxlim[1] - vxlim[0]) <= 5 || Math.abs(vylim[1] - vylim[0]) <= 5) {
      return;
    }
    xrs = {};
    ref = this.plot_view.frame.get('x_mappers');
    for (name in ref) {
      mapper = ref[name];
      ref1 = mapper.v_map_from_target(vxlim, true), start = ref1[0], end = ref1[1];
      xrs[name] = {
        start: start,
        end: end
      };
    }
    yrs = {};
    ref2 = this.plot_view.frame.get('y_mappers');
    for (name in ref2) {
      mapper = ref2[name];
      ref3 = mapper.v_map_from_target(vylim, true), start = ref3[0], end = ref3[1];
      yrs[name] = {
        start: start,
        end: end
      };
    }
    zoom_info = {
      xrs: xrs,
      yrs: yrs
    };
    this.plot_view.push_state('box_zoom', {
      range: zoom_info
    });
    return this.plot_view.update_range(zoom_info);
  };

  return BoxZoomToolView;

})(GestureTool.View);

BoxZoomTool = (function(superClass) {
  extend(BoxZoomTool, superClass);

  function BoxZoomTool() {
    return BoxZoomTool.__super__.constructor.apply(this, arguments);
  }

  BoxZoomTool.prototype.default_view = BoxZoomToolView;

  BoxZoomTool.prototype.type = "BoxZoomTool";

  BoxZoomTool.prototype.tool_name = "Box Zoom";

  BoxZoomTool.prototype.icon = "bk-tool-icon-box-zoom";

  BoxZoomTool.prototype.event_type = "pan";

  BoxZoomTool.prototype.default_order = 20;

  BoxZoomTool.prototype.initialize = function(attrs, options) {
    BoxZoomTool.__super__.initialize.call(this, attrs, options);
    this.get('overlay').set('silent_update', true, {
      silent: true
    });
    this.register_property('tooltip', function() {
      return this._get_dim_tooltip(this.get("tool_name"), this._check_dims(this.get('dimensions'), "box zoom tool"));
    }, false);
    return this.add_dependencies('tooltip', this, ['dimensions']);
  };

  BoxZoomTool.prototype.defaults = function() {
    return _.extend({}, BoxZoomTool.__super__.defaults.call(this), {
      dimensions: ["width", "height"],
      overlay: new BoxAnnotation.Model({
        level: "overlay",
        render_mode: "css",
        top_units: "screen",
        left_units: "screen",
        bottom_units: "screen",
        right_units: "screen",
        fill_color: "lightgrey",
        fill_alpha: 0.5,
        line_color: "black",
        line_alpha: 1.0,
        line_width: 2,
        line_dash: [4, 4]
      })
    });
  };

  return BoxZoomTool;

})(GestureTool.Model);

module.exports = {
  Model: BoxZoomTool,
  View: BoxZoomToolView
};
