var GestureTool, SelectTool, SelectToolView, _, logger,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

logger = require("../../../common/logging").logger;

GestureTool = require("./gesture_tool");

SelectToolView = (function(superClass) {
  extend(SelectToolView, superClass);

  function SelectToolView() {
    return SelectToolView.__super__.constructor.apply(this, arguments);
  }

  SelectToolView.prototype._keyup = function(e) {
    var ds, j, len, r, ref, results, sm;
    if (e.keyCode === 27) {
      ref = this.mget('renderers');
      results = [];
      for (j = 0, len = ref.length; j < len; j++) {
        r = ref[j];
        ds = r.get('data_source');
        sm = ds.get('selection_manager');
        results.push(sm.clear());
      }
      return results;
    }
  };

  SelectToolView.prototype._save_geometry = function(geometry, final, append) {
    var g, geoms, i, j, ref, tool_events, xm, ym;
    g = _.clone(geometry);
    xm = this.plot_view.frame.get('x_mappers')['default'];
    ym = this.plot_view.frame.get('y_mappers')['default'];
    if (g.type === 'point') {
      g.x = xm.map_from_target(g.vx);
      g.y = ym.map_from_target(g.vy);
    } else if (g.type === 'rect') {
      g.x0 = xm.map_from_target(g.vx0);
      g.y0 = ym.map_from_target(g.vy0);
      g.x1 = xm.map_from_target(g.vx1);
      g.y1 = ym.map_from_target(g.vy1);
    } else if (g.type === 'poly') {
      g.x = new Array(g.vx.length);
      g.y = new Array(g.vy.length);
      for (i = j = 0, ref = g.vx.length; 0 <= ref ? j < ref : j > ref; i = 0 <= ref ? ++j : --j) {
        g.x[i] = xm.map_from_target(g.vx[i]);
        g.y[i] = ym.map_from_target(g.vy[i]);
      }
    } else {
      logger.debug("Unrecognized selection geometry type: '" + g.type + "'");
    }
    if (final) {
      tool_events = this.plot_model.get('tool_events');
      if (append) {
        geoms = tool_events.get('geometries');
        geoms.push(g);
      } else {
        geoms = [g];
      }
      tool_events.set("geometries", geoms);
    }
    return null;
  };

  return SelectToolView;

})(GestureTool.View);

SelectTool = (function(superClass) {
  extend(SelectTool, superClass);

  function SelectTool() {
    return SelectTool.__super__.constructor.apply(this, arguments);
  }

  SelectTool.prototype.initialize = function(attrs, options) {
    var all_renderers, j, len, names, r, renderers;
    SelectTool.__super__.initialize.call(this, attrs, options);
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
    this.set('renderers', renderers);
    logger.debug("setting " + renderers.length + " renderers for " + this.type + " " + this.id);
    for (j = 0, len = renderers.length; j < len; j++) {
      r = renderers[j];
      logger.debug(" - " + r.type + " " + r.id);
    }
    return null;
  };

  SelectTool.prototype.nonserializable_attribute_names = function() {
    return SelectTool.__super__.nonserializable_attribute_names.call(this).concat(['multi_select_modifier']);
  };

  SelectTool.prototype.defaults = function() {
    return _.extend({}, SelectTool.__super__.defaults.call(this), {
      renderers: [],
      names: [],
      multi_select_modifier: "shift"
    });
  };

  return SelectTool;

})(GestureTool.Model);

module.exports = {
  Model: SelectTool,
  View: SelectToolView
};
