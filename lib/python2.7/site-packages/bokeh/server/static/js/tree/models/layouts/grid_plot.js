var $, Backbone, Component, ContinuumView, GridPlot, GridPlotView, GridToolManager, GridViewState, HasProps, ToolManager, ToolProxy, _, build_views, logger, plot_template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

$ = require("jquery");

_ = require("underscore");

Backbone = require("backbone");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

Component = require("../component");

HasProps = require("../../common/has_props");

logger = require("../../common/logging").logger;

ToolManager = require("../../common/tool_manager");

plot_template = require("../../common/plot_template");

ToolProxy = (function(superClass) {
  extend(ToolProxy, superClass);

  function ToolProxy() {
    return ToolProxy.__super__.constructor.apply(this, arguments);
  }

  ToolProxy.prototype.initialize = function(options) {
    ToolProxy.__super__.initialize.call(this, options);
    this.listenTo(this, 'do', this["do"]);
    this.listenTo(this, 'change:active', this.active);
    return null;
  };

  ToolProxy.prototype["do"] = function() {
    var i, len, ref, tool;
    ref = this.attributes.tools;
    for (i = 0, len = ref.length; i < len; i++) {
      tool = ref[i];
      tool.trigger('do');
    }
    return null;
  };

  ToolProxy.prototype.active = function() {
    var i, len, ref, tool;
    ref = this.attributes.tools;
    for (i = 0, len = ref.length; i < len; i++) {
      tool = ref[i];
      tool.set('active', this.attributes.active);
    }
    return null;
  };

  ToolProxy.prototype.attrs_and_props = function() {
    return this.attributes.tools[0].attrs_and_props();
  };

  ToolProxy.prototype.get = function(attr) {
    return this.attributes.tools[0].get(attr);
  };

  ToolProxy.prototype.set = function(attr, value) {
    var i, len, ref, tool;
    ToolProxy.__super__.set.call(this, attr, value);
    attr = _.omit(attr, "tools");
    ref = this.attributes.tools;
    for (i = 0, len = ref.length; i < len; i++) {
      tool = ref[i];
      tool.set(attr, value);
    }
    return null;
  };

  return ToolProxy;

})(Backbone.Model);

GridToolManager = (function(superClass) {
  extend(GridToolManager, superClass);

  function GridToolManager() {
    this._active_change = bind(this._active_change, this);
    return GridToolManager.__super__.constructor.apply(this, arguments);
  }

  GridToolManager.prototype._init_tools = function() {
    var actions, et, gestures, i, info, inspectors, j, k, l, len, len1, len2, len3, proxy, ref, ref1, ref2, ref3, ref4, ref5, ref6, results, tm, tmp, tool, tools, typ;
    inspectors = {};
    actions = {};
    gestures = {};
    ref = this.get('tool_managers');
    for (i = 0, len = ref.length; i < len; i++) {
      tm = ref[i];
      ref1 = tm.get('gestures');
      for (et in ref1) {
        info = ref1[et];
        if (!(et in gestures)) {
          gestures[et] = {};
        }
        ref2 = info.tools;
        for (j = 0, len1 = ref2.length; j < len1; j++) {
          tool = ref2[j];
          if (!(tool.type in gestures[et])) {
            gestures[et][tool.type] = [];
          }
          gestures[et][tool.type].push(tool);
        }
      }
      ref3 = tm.get('inspectors');
      for (k = 0, len2 = ref3.length; k < len2; k++) {
        tool = ref3[k];
        if (!(tool.type in inspectors)) {
          inspectors[tool.type] = [];
        }
        inspectors[tool.type].push(tool);
      }
      ref4 = tm.get('actions');
      for (l = 0, len3 = ref4.length; l < len3; l++) {
        tool = ref4[l];
        if (!(tool.type in actions)) {
          actions[tool.type] = [];
        }
        actions[tool.type].push(tool);
      }
    }
    for (et in gestures) {
      ref5 = gestures[et];
      for (typ in ref5) {
        tools = ref5[typ];
        if (tools.length !== this.get('num_plots')) {
          continue;
        }
        proxy = new ToolProxy({
          tools: tools
        });
        this.get('gestures')[et].tools.push(proxy);
        this.listenTo(proxy, 'change:active', _.bind(this._active_change, proxy));
      }
    }
    for (typ in actions) {
      tools = actions[typ];
      if (tools.length !== this.get('num_plots')) {
        continue;
      }
      proxy = new ToolProxy({
        tools: tools
      });
      tmp = this.get('actions');
      tmp.push(proxy);
      this.set('actions', tmp);
    }
    for (typ in inspectors) {
      tools = inspectors[typ];
      if (tools.length !== this.get('num_plots')) {
        continue;
      }
      proxy = new ToolProxy({
        tools: tools
      });
      tmp = this.get('inspectors');
      tmp.push(proxy);
      this.set('inspectors', tmp);
    }
    ref6 = this.get('gestures');
    results = [];
    for (et in ref6) {
      info = ref6[et];
      tools = info.tools;
      if (tools.length === 0) {
        continue;
      }
      info.tools = _.sortBy(tools, function(tool) {
        return tool.get('default_order');
      });
      if (et !== 'pinch' && et !== 'scroll') {
        results.push(info.tools[0].set('active', true));
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  GridToolManager.prototype._active_change = function(tool) {
    var currently_active_tool, event_type, gestures;
    event_type = tool.get('event_type');
    gestures = this.get('gestures');
    currently_active_tool = gestures[event_type].active;
    if ((currently_active_tool != null) && currently_active_tool !== tool) {
      logger.debug("GridToolManager: deactivating tool: " + currently_active_tool.type + " (" + currently_active_tool.id + ") for event type '" + event_type + "'");
      currently_active_tool.set('active', false);
    }
    gestures[event_type].active = tool;
    this.set('gestures', gestures);
    logger.debug("GridToolManager: activating tool: " + tool.type + " (" + tool.id + ") for event type '" + event_type + "'");
    return null;
  };

  GridToolManager.prototype.defaults = function() {
    return _.extend({}, GridToolManager.__super__.defaults.call(this), {
      tool_manangers: []
    });
  };

  return GridToolManager;

})(ToolManager.Model);

GridViewState = (function(superClass) {
  extend(GridViewState, superClass);

  function GridViewState() {
    this.layout_widths = bind(this.layout_widths, this);
    this.layout_heights = bind(this.layout_heights, this);
    this.setup_layout_properties = bind(this.setup_layout_properties, this);
    return GridViewState.__super__.constructor.apply(this, arguments);
  }

  GridViewState.prototype.setup_layout_properties = function() {
    var i, len, ref, results, row, viewstate;
    this.register_property('layout_heights', this.layout_heights, false);
    this.register_property('layout_widths', this.layout_widths, false);
    ref = this.get('viewstates');
    results = [];
    for (i = 0, len = ref.length; i < len; i++) {
      row = ref[i];
      results.push((function() {
        var j, len1, results1;
        results1 = [];
        for (j = 0, len1 = row.length; j < len1; j++) {
          viewstate = row[j];
          this.add_dependencies('layout_heights', viewstate, 'height');
          results1.push(this.add_dependencies('layout_widths', viewstate, 'width'));
        }
        return results1;
      }).call(this));
    }
    return results;
  };

  GridViewState.prototype.initialize = function(attrs, options) {
    var calculateHeight, calculateWidth;
    GridViewState.__super__.initialize.call(this, attrs, options);
    this.setup_layout_properties();
    this.listenTo(this, 'change:viewstates', this.setup_layout_properties);
    calculateHeight = (function(_this) {
      return function() {
        return _.reduce(_this.get("layout_heights"), (function(x, y) {
          return x + y;
        }), 0);
      };
    })(this);
    this.register_property('height', calculateHeight, false);
    this.add_dependencies('height', this, 'layout_heights');
    calculateWidth = (function(_this) {
      return function() {
        return _.reduce(_this.get("layout_widths"), (function(x, y) {
          return x + y;
        }), 0);
      };
    })(this);
    this.register_property('width', calculateWidth, false);
    return this.add_dependencies('width', this, 'layout_widths');
  };

  GridViewState.prototype.position_child_x = function(offset, childsize) {
    return offset;
  };

  GridViewState.prototype.position_child_y = function(offset, childsize) {
    return this.get('height') - offset - childsize;
  };

  GridViewState.prototype.maxdim = function(dim, row) {
    if (row.length === 0) {
      return 0;
    } else {
      return _.max(_.map(row, function(x) {
        if (x != null) {
          return x.get(dim);
        }
        return 0;
      }));
    }
  };

  GridViewState.prototype.layout_heights = function() {
    var row, row_heights;
    row_heights = (function() {
      var i, len, ref, results;
      ref = this.get('viewstates');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        row = ref[i];
        results.push(this.maxdim('height', row));
      }
      return results;
    }).call(this);
    return row_heights;
  };

  GridViewState.prototype.layout_widths = function() {
    var col, col_widths, columns, n, num_cols, row;
    num_cols = this.get('viewstates')[0].length;
    columns = (function() {
      var i, len, ref, results;
      ref = _.range(num_cols);
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        n = ref[i];
        results.push((function() {
          var j, len1, ref1, results1;
          ref1 = this.get('viewstates');
          results1 = [];
          for (j = 0, len1 = ref1.length; j < len1; j++) {
            row = ref1[j];
            results1.push(row[n]);
          }
          return results1;
        }).call(this));
      }
      return results;
    }).call(this);
    col_widths = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = columns.length; i < len; i++) {
        col = columns[i];
        results.push(this.maxdim('width', col));
      }
      return results;
    }).call(this);
    return col_widths;
  };

  GridViewState.prototype.defaults = function() {
    return _.extend({}, GridViewState.__super__.defaults.call(this), {
      viewstates: [[]],
      border_space: 0
    });
  };

  return GridViewState;

})(HasProps);

GridPlotView = (function(superClass) {
  extend(GridPlotView, superClass);

  function GridPlotView() {
    return GridPlotView.__super__.constructor.apply(this, arguments);
  }

  GridPlotView.prototype.className = "";

  GridPlotView.prototype.template = plot_template;

  GridPlotView.prototype.initialize = function(options) {
    var toolbar_location, toolbar_selector;
    GridPlotView.__super__.initialize.call(this, options);
    this.viewstate = new GridViewState();
    this.child_views = {};
    this.build_children();
    this.bind_bokeh_events();
    this.$el.html(this.template());
    toolbar_location = this.mget('toolbar_location');
    if (toolbar_location != null) {
      toolbar_selector = '.bk-plot-' + toolbar_location;
      logger.debug("attaching toolbar to " + toolbar_selector + " for plot " + this.model.id);
      this.tm_view = new ToolManager.View({
        model: this.mget('tool_manager'),
        el: this.$(toolbar_selector)
      });
    }
    this.render();
    return this;
  };

  GridPlotView.prototype.bind_bokeh_events = function() {
    this.listenTo(this.model, 'change:children', this.build_children);
    this.listenTo(this.model, 'change', this.render);
    this.listenTo(this.viewstate, 'change', this.render);
    return this.listenTo(this.model, 'destroy', this.remove);
  };

  GridPlotView.prototype.build_children = function() {
    var childmodels, i, j, k, l, len, len1, len2, len3, len4, m, plot, ref, ref1, ref2, results, row, viewstates, vsrow;
    childmodels = [];
    ref = this.mget('children');
    for (i = 0, len = ref.length; i < len; i++) {
      row = ref[i];
      for (j = 0, len1 = row.length; j < len1; j++) {
        plot = row[j];
        if (plot == null) {
          continue;
        }
        plot.set('toolbar_location', null);
        childmodels.push(plot);
      }
    }
    build_views(this.child_views, childmodels, {});
    viewstates = [];
    ref1 = this.mget('children');
    for (k = 0, len2 = ref1.length; k < len2; k++) {
      row = ref1[k];
      vsrow = [];
      for (l = 0, len3 = row.length; l < len3; l++) {
        plot = row[l];
        if (plot == null) {
          continue;
        }
        vsrow.push(this.child_views[plot.id].canvas);
      }
      viewstates.push(vsrow);
    }
    this.viewstate.set('viewstates', viewstates);
    ref2 = this.mget('children');
    results = [];
    for (m = 0, len4 = ref2.length; m < len4; m++) {
      row = ref2[m];
      results.push((function() {
        var len5, o, results1;
        results1 = [];
        for (o = 0, len5 = row.length; o < len5; o++) {
          plot = row[o];
          if (plot == null) {
            continue;
          }
          results1.push(this.listenTo(plot.solver, 'layout_update', this.render));
        }
        return results1;
      }).call(this));
    }
    return results;
  };

  GridPlotView.prototype.render = function() {
    var add, cidx, col_widths, div, height, i, j, k, last_plot, len, len1, len2, plot, plot_divs, plot_wrapper, ref, ref1, ridx, row, row_heights, toolbar_location, toolbar_selector, total_height, view, width, x_coords, xpos, y_coords, ypos;
    GridPlotView.__super__.render.call(this);
    ref = _.values(this.child_views);
    for (i = 0, len = ref.length; i < len; i++) {
      view = ref[i];
      view.$el.detach();
    }
    div = $('<div />');
    this.$('.bk-plot-canvas-wrapper').empty();
    this.$('.bk-plot-canvas-wrapper').append(div);
    toolbar_location = this.mget('toolbar_location');
    if (toolbar_location != null) {
      toolbar_selector = '.bk-plot-' + toolbar_location;
      this.tm_view = new ToolManager.View({
        model: this.mget('tool_manager'),
        el: this.$(toolbar_selector)
      });
      this.tm_view.render();
    }
    row_heights = this.viewstate.get('layout_heights');
    col_widths = this.viewstate.get('layout_widths');
    y_coords = [0];
    _.reduceRight(row_heights.slice(1), function(x, y) {
      var val;
      val = x + y;
      y_coords.push(val);
      return val;
    }, 0);
    y_coords.reverse();
    x_coords = [0];
    _.reduce(col_widths.slice(0), function(x, y) {
      var val;
      val = x + y;
      x_coords.push(val);
      return val;
    }, 0);
    plot_divs = [];
    last_plot = null;
    ref1 = this.mget('children');
    for (ridx = j = 0, len1 = ref1.length; j < len1; ridx = ++j) {
      row = ref1[ridx];
      for (cidx = k = 0, len2 = row.length; k < len2; cidx = ++k) {
        plot = row[cidx];
        if (plot == null) {
          continue;
        }
        view = this.child_views[plot.id];
        ypos = this.viewstate.position_child_y(y_coords[ridx], view.canvas.get('height'));
        xpos = this.viewstate.position_child_x(x_coords[cidx], view.canvas.get('width'));
        plot_wrapper = $("<div class='gp_plotwrapper'></div>");
        plot_wrapper.attr('style', "position: absolute; left:" + xpos + "px; top:" + ypos + "px");
        plot_wrapper.append(view.$el);
        div.append(plot_wrapper);
      }
    }
    add = function(a, b) {
      return a + b;
    };
    total_height = _.reduce(row_heights, add, 0);
    height = total_height;
    width = _.reduce(col_widths, add, 0);
    return div.attr('style', "position:relative; height:" + height + "px;width:" + width + "px");
  };

  return GridPlotView;

})(ContinuumView);

GridPlot = (function(superClass) {
  extend(GridPlot, superClass);

  function GridPlot() {
    return GridPlot.__super__.constructor.apply(this, arguments);
  }

  GridPlot.prototype.type = 'GridPlot';

  GridPlot.prototype.default_view = GridPlotView;

  GridPlot.prototype.initialize = function(attrs, options) {
    GridPlot.__super__.initialize.call(this, attrs, options);
    return this.register_property('tool_manager', function() {
      var children, i, len, plot, ref;
      children = [];
      ref = _.flatten(this.get('children'));
      for (i = 0, len = ref.length; i < len; i++) {
        plot = ref[i];
        if (plot != null) {
          children.push(plot);
        }
      }
      return new GridToolManager({
        tool_managers: (function() {
          var j, len1, results;
          results = [];
          for (j = 0, len1 = children.length; j < len1; j++) {
            plot = children[j];
            results.push(plot.get('tool_manager'));
          }
          return results;
        })(),
        toolbar_location: this.get('toolbar_location'),
        num_plots: children.length
      });
    }, true);
  };

  GridPlot.prototype.defaults = function() {
    return _.extend({}, GridPlot.__super__.defaults.call(this), {
      children: [[]],
      border_space: 0,
      toolbar_location: "left",
      disabled: false
    });
  };

  return GridPlot;

})(Component.Model);

module.exports = {
  Model: GridPlot,
  View: GridPlotView
};
