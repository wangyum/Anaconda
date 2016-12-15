var SelectTool, TapTool, TapToolView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

SelectTool = require("./select_tool");

TapToolView = (function(superClass) {
  extend(TapToolView, superClass);

  function TapToolView() {
    return TapToolView.__super__.constructor.apply(this, arguments);
  }

  TapToolView.prototype._tap = function(e) {
    var append, canvas, ref, vx, vy;
    canvas = this.plot_view.canvas;
    vx = canvas.sx_to_vx(e.bokeh.sx);
    vy = canvas.sy_to_vy(e.bokeh.sy);
    append = (ref = e.srcEvent.shiftKey) != null ? ref : false;
    return this._select(vx, vy, true, append);
  };

  TapToolView.prototype._select = function(vx, vy, final, append) {
    var callback, ds, geometry, i, len, r, ref, sm;
    geometry = {
      type: 'point',
      vx: vx,
      vy: vy
    };
    callback = this.mget("callback");
    ref = this.mget('renderers');
    for (i = 0, len = ref.length; i < len; i++) {
      r = ref[i];
      ds = r.get('data_source');
      sm = ds.get('selection_manager');
      sm.select(this, this.plot_view.renderers[r.id], geometry, final, append);
      if (callback != null) {
        callback.execute(ds);
      }
    }
    this._save_geometry(geometry, final, append);
    this.plot_view.push_state('tap', {
      selection: this.plot_view.get_selection()
    });
    return null;
  };

  return TapToolView;

})(SelectTool.View);

TapTool = (function(superClass) {
  extend(TapTool, superClass);

  function TapTool() {
    return TapTool.__super__.constructor.apply(this, arguments);
  }

  TapTool.prototype.default_view = TapToolView;

  TapTool.prototype.type = "TapTool";

  TapTool.prototype.tool_name = "Tap";

  TapTool.prototype.icon = "bk-tool-icon-tap-select";

  TapTool.prototype.event_type = "tap";

  TapTool.prototype.default_order = 10;

  TapTool.prototype.defaults = function() {
    return _.extend({}, TapTool.__super__.defaults.call(this), {
      callback: null
    });
  };

  return TapTool;

})(SelectTool.Model);

module.exports = {
  Model: TapTool,
  View: TapToolView
};
