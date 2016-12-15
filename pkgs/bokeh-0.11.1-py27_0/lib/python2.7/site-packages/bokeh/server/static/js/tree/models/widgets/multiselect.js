var $, ContinuumView, InputWidget, MultiSelect, MultiSelectView, _, multiselecttemplate,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("jquery");

$ = require("underscore");

ContinuumView = require("../../common/continuum_view");

multiselecttemplate = require("./multiselecttemplate");

InputWidget = require("./input_widget");

MultiSelectView = (function(superClass) {
  extend(MultiSelectView, superClass);

  function MultiSelectView() {
    this.render_selection = bind(this.render_selection, this);
    return MultiSelectView.__super__.constructor.apply(this, arguments);
  }

  MultiSelectView.prototype.tagName = "div";

  MultiSelectView.prototype.template = multiselecttemplate;

  MultiSelectView.prototype.events = {
    "change select": "change_input"
  };

  MultiSelectView.prototype.initialize = function(options) {
    MultiSelectView.__super__.initialize.call(this, options);
    this.render();
    this.listenTo(this.model, 'change:value', this.render_selection);
    this.listenTo(this.model, 'change:options', this.render);
    this.listenTo(this.model, 'change:name', this.render);
    return this.listenTo(this.model, 'change:title', this.render);
  };

  MultiSelectView.prototype.render = function() {
    var html;
    this.$el.empty();
    html = this.template(this.model.attributes);
    this.$el.html(html);
    this.render_selection();
    return this;
  };

  MultiSelectView.prototype.render_selection = function() {
    var values;
    values = {};
    _.map(this.mget('value'), function(x) {
      return values[x] = true;
    });
    return this.$('option').each((function(_this) {
      return function(el) {
        el = _this.$(el);
        if (values[el.attr('value')]) {
          return el.attr('selected', 'selected');
        }
      };
    })(this));
  };

  MultiSelectView.prototype.change_input = function() {
    var ref;
    this.mset('value', this.$('select').val(), {
      'silent': true
    });
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return MultiSelectView;

})(ContinuumView);

MultiSelect = (function(superClass) {
  extend(MultiSelect, superClass);

  function MultiSelect() {
    return MultiSelect.__super__.constructor.apply(this, arguments);
  }

  MultiSelect.prototype.type = "MultiSelect";

  MultiSelect.prototype.default_view = MultiSelectView;

  MultiSelect.prototype.defaults = function() {
    return _.extend({}, MultiSelect.__super__.defaults.call(this), {
      title: '',
      value: [],
      options: []
    });
  };

  return MultiSelect;

})(InputWidget.Model);

module.exports = {
  Model: MultiSelect,
  View: MultiSelectView
};
