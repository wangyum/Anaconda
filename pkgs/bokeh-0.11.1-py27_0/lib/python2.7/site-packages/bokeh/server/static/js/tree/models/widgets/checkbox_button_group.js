var $, $1, CheckboxButtonGroup, CheckboxButtonGroupView, ContinuumView, Model, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty,
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

_ = require("underscore");

$ = require("jquery");

$1 = require("bootstrap/button");

ContinuumView = require("../../common/continuum_view");

Model = require("../../model");

CheckboxButtonGroupView = (function(superClass) {
  extend(CheckboxButtonGroupView, superClass);

  function CheckboxButtonGroupView() {
    return CheckboxButtonGroupView.__super__.constructor.apply(this, arguments);
  }

  CheckboxButtonGroupView.prototype.tagName = "div";

  CheckboxButtonGroupView.prototype.events = {
    "change input": "change_input"
  };

  CheckboxButtonGroupView.prototype.initialize = function(options) {
    CheckboxButtonGroupView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  CheckboxButtonGroupView.prototype.render = function() {
    var $input, $label, active, i, j, label, len, ref;
    this.$el.empty();
    this.$el.addClass("bk-bs-btn-group");
    this.$el.attr("data-bk-bs-toggle", "buttons");
    active = this.mget("active");
    ref = this.mget("labels");
    for (i = j = 0, len = ref.length; j < len; i = ++j) {
      label = ref[i];
      $input = $('<input type="checkbox">').attr({
        value: "" + i
      });
      if (indexOf.call(active, i) >= 0) {
        $input.prop("checked", true);
      }
      $label = $('<label class="bk-bs-btn"></label>');
      $label.text(label).prepend($input);
      $label.addClass("bk-bs-btn-" + this.mget("type"));
      if (indexOf.call(active, i) >= 0) {
        $label.addClass("bk-bs-active");
      }
      this.$el.append($label);
    }
    return this;
  };

  CheckboxButtonGroupView.prototype.change_input = function() {
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

  return CheckboxButtonGroupView;

})(ContinuumView);

CheckboxButtonGroup = (function(superClass) {
  extend(CheckboxButtonGroup, superClass);

  function CheckboxButtonGroup() {
    return CheckboxButtonGroup.__super__.constructor.apply(this, arguments);
  }

  CheckboxButtonGroup.prototype.type = "CheckboxButtonGroup";

  CheckboxButtonGroup.prototype.default_view = CheckboxButtonGroupView;

  CheckboxButtonGroup.prototype.defaults = function() {
    return _.extend({}, CheckboxButtonGroup.__super__.defaults.call(this), {
      active: [],
      labels: [],
      type: "default",
      disabled: false
    });
  };

  return CheckboxButtonGroup;

})(Model);

module.exports = {
  Model: CheckboxButtonGroup,
  View: CheckboxButtonGroupView
};
