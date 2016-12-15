var $, $$1, ActionTool, Backbone, GestureTool, HasProps, HelpTool, InspectTool, ToolManager, ToolManagerView, _, logger, toolbar_template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

_ = require("underscore");

$ = require("jquery");

$$1 = require("bootstrap/dropdown");

Backbone = require("backbone");

ActionTool = require("../models/tools/actions/action_tool");

HelpTool = require("../models/tools/actions/help_tool");

GestureTool = require("../models/tools/gestures/gesture_tool");

InspectTool = require("../models/tools/inspectors/inspect_tool");

logger = require("./logging").logger;

toolbar_template = require("./toolbar_template");

HasProps = require("./has_props");

ToolManagerView = (function(superClass) {
  extend(ToolManagerView, superClass);

  function ToolManagerView() {
    return ToolManagerView.__super__.constructor.apply(this, arguments);
  }

  ToolManagerView.prototype.template = toolbar_template;

  ToolManagerView.prototype.initialize = function(options) {
    ToolManagerView.__super__.initialize.call(this, options);
    this.listenTo(this.model, 'change', this.render);
    return this.have_rendered = false;
  };

  ToolManagerView.prototype.render = function() {
    var anchor, button_bar_list, et, gestures, inspectors, ul;
    if (this.have_rendered) {
      return;
    }
    this.have_rendered = true;
    this.$el.html(this.template(this.model.attributes));
    this.$el.addClass("bk-sidebar");
    this.$el.addClass("bk-toolbar-active");
    button_bar_list = this.$('.bk-button-bar-list');
    inspectors = this.model.get('inspectors');
    button_bar_list = this.$(".bk-bs-dropdown[type='inspectors']");
    if (inspectors.length === 0) {
      button_bar_list.hide();
    } else {
      anchor = $('<a href="#" data-bk-bs-toggle="dropdown" class="bk-bs-dropdown-toggle">inspect <span class="bk-bs-caret"></a>');
      anchor.appendTo(button_bar_list);
      ul = $('<ul class="bk-bs-dropdown-menu" />');
      _.each(inspectors, function(tool) {
        var item;
        item = $('<li />');
        item.append(new InspectTool.ListItemView({
          model: tool
        }).el);
        return item.appendTo(ul);
      });
      ul.on('click', function(e) {
        return e.stopPropagation();
      });
      ul.appendTo(button_bar_list);
      anchor.dropdown();
    }
    button_bar_list = this.$(".bk-button-bar-list[type='help']");
    _.each(this.model.get('help'), function(item) {
      return button_bar_list.append(new ActionTool.ButtonView({
        model: item
      }).el);
    });
    button_bar_list = this.$(".bk-button-bar-list[type='actions']");
    _.each(this.model.get('actions'), function(item) {
      return button_bar_list.append(new ActionTool.ButtonView({
        model: item
      }).el);
    });
    gestures = this.model.get('gestures');
    for (et in gestures) {
      button_bar_list = this.$(".bk-button-bar-list[type='" + et + "']");
      _.each(gestures[et].tools, function(item) {
        return button_bar_list.append(new GestureTool.ButtonView({
          model: item
        }).el);
      });
    }
    return this;
  };

  return ToolManagerView;

})(Backbone.View);

ToolManager = (function(superClass) {
  extend(ToolManager, superClass);

  function ToolManager() {
    this._active_change = bind(this._active_change, this);
    return ToolManager.__super__.constructor.apply(this, arguments);
  }

  ToolManager.prototype.type = 'ToolManager';

  ToolManager.prototype.initialize = function(attrs, options) {
    ToolManager.__super__.initialize.call(this, attrs, options);
    return this._init_tools();
  };

  ToolManager.prototype.serializable_in_document = function() {
    return false;
  };

  ToolManager.prototype._init_tools = function() {
    var actions, et, gestures, help, i, inspectors, len, ref, results, tool, tools;
    gestures = this.get('gestures');
    ref = this.get('tools');
    for (i = 0, len = ref.length; i < len; i++) {
      tool = ref[i];
      if (tool instanceof InspectTool.Model) {
        inspectors = this.get('inspectors');
        inspectors.push(tool);
        this.set('inspectors', inspectors);
      } else if (tool instanceof HelpTool.Model) {
        help = this.get('help');
        help.push(tool);
        this.set('help', help);
      } else if (tool instanceof ActionTool.Model) {
        actions = this.get('actions');
        actions.push(tool);
        this.set('actions', actions);
      } else if (tool instanceof GestureTool.Model) {
        et = tool.get('event_type');
        if (!(et in gestures)) {
          logger.warn("ToolManager: unknown event type '" + et + "' for tool: " + tool.type + " (" + tool.id + ")");
          continue;
        }
        gestures[et].tools.push(tool);
        this.listenTo(tool, 'change:active', _.bind(this._active_change, tool));
      }
    }
    results = [];
    for (et in gestures) {
      tools = gestures[et].tools;
      if (tools.length === 0) {
        continue;
      }
      gestures[et].tools = _.sortBy(tools, function(tool) {
        return tool.get('default_order');
      });
      if (et !== 'pinch' && et !== 'scroll') {
        results.push(gestures[et].tools[0].set('active', true));
      } else {
        results.push(void 0);
      }
    }
    return results;
  };

  ToolManager.prototype._active_change = function(tool) {
    var currently_active_tool, event_type, gestures;
    event_type = tool.get('event_type');
    gestures = this.get('gestures');
    currently_active_tool = gestures[event_type].active;
    if ((currently_active_tool != null) && currently_active_tool !== tool) {
      logger.debug("ToolManager: deactivating tool: " + currently_active_tool.type + " (" + currently_active_tool.id + ") for event type '" + event_type + "'");
      currently_active_tool.set('active', false);
    }
    gestures[event_type].active = tool;
    this.set('gestures', gestures);
    logger.debug("ToolManager: activating tool: " + tool.type + " (" + tool.id + ") for event type '" + event_type + "'");
    return null;
  };

  ToolManager.prototype.defaults = function() {
    return {
      gestures: {
        pan: {
          tools: [],
          active: null
        },
        tap: {
          tools: [],
          active: null
        },
        doubletap: {
          tools: [],
          active: null
        },
        scroll: {
          tools: [],
          active: null
        },
        pinch: {
          tools: [],
          active: null
        },
        press: {
          tools: [],
          active: null
        },
        rotate: {
          tools: [],
          active: null
        }
      },
      actions: [],
      inspectors: [],
      help: []
    };
  };

  return ToolManager;

})(HasProps);

module.exports = {
  Model: ToolManager,
  View: ToolManagerView
};
