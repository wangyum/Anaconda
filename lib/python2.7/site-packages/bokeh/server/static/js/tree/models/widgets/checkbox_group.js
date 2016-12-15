var $, CheckboxGroup, CheckboxGroupView, ContinuumView, Model, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

_ = require("underscore");

$ = require("jquery");

ContinuumView = require("../../common/continuum_view");

Model = require("../../model");

CheckboxGroupView = (function(superClass) {
  extend(CheckboxGroupView, superClass);

  function CheckboxGroupView() {
    return CheckboxGroupView.__super__.constructor.apply(this, arguments);
  }

  CheckboxGroupView.prototype.tagName = "div";

  CheckboxGroupView.prototype.events = {
    "change input": "change_input"
  };

  CheckboxGroupView.prototype.initialize = function(options) {
    CheckboxGroupView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  CheckboxGroupView.prototype.render = function() {
    var $div, $input, $label, active, i, j, label, len, ref;
    this.$el.empty();
    active = this.mget("active");
    ref = this.mget("labels");
    for (i = j = 0, len = ref.length; j < len; i = ++j) {
      label = ref[i];
      $input = $('<input type="checkbox">').attr({
        value: "" + i
      });
      if (this.mget("disabled")) {
        $input.prop("disabled", true);
      }
      if (indexOf.call(active, i) >= 0) {
        $input.prop("checked", true);
      }
      $label = $('<label></label>').text(label).prepend($input);
      if (this.mget("inline")) {
        $label.addClass("bk-bs-checkbox-inline");
        this.$el.append($label);
      } else {
        $div = $('<div class="bk-bs-checkbox"></div>').append($label);
        this.$el.append($div);
      }
    }
    return this;
  };

  CheckboxGroupView.prototype.change_input = function() {
    var active, checkbox, i, ref;
    active = (function() {
      var j, len, ref, results;
      ref = this.$("input");
      results = [];
      for (i = j = 0, len = ref.length; j < len; i = ++j) {
        checkbox = ref[i];
        if (checkbox.checked) {
          results.push(i);
        }
      }
      return results;
    }).call(this);
    this.mset('active', active);
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return CheckboxGroupView;

})(ContinuumView);

CheckboxGroup = (function(superClass) {
  extend(CheckboxGroup, superClass);

  function CheckboxGroup() {
    return CheckboxGroup.__super__.constructor.apply(this, arguments);
  }

  CheckboxGroup.prototype.type = "CheckboxGroup";

  CheckboxGroup.prototype.default_view = CheckboxGroupView;

  CheckboxGroup.prototype.defaults = function() {
    return _.extend({}, CheckboxGroup.__super__.defaults.call(this), {
      active: [],
      labels: [],
      inline: false,
      disabled: false
    });
  };

  return CheckboxGroup;

})(Model);

module.exports = {
  Model: CheckboxGroup,
  View: CheckboxGroupView
};
