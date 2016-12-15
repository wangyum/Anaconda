var $, $1, ContinuumView, DatePicker, DatePickerView, InputWidget, _,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

$1 = require("jquery-ui/datepicker");

ContinuumView = require("../../common/continuum_view");

InputWidget = require("./input_widget");

DatePickerView = (function(superClass) {
  extend(DatePickerView, superClass);

  function DatePickerView() {
    this.onSelect = bind(this.onSelect, this);
    return DatePickerView.__super__.constructor.apply(this, arguments);
  }

  DatePickerView.prototype.initialize = function(options) {
    DatePickerView.__super__.initialize.call(this, options);
    return this.render();
  };

  DatePickerView.prototype.render = function() {
    var $datepicker, $label;
    this.$el.empty();
    $label = $('<label>').text(this.mget("title"));
    $datepicker = $("<div>").datepicker({
      defaultDate: new Date(this.mget('value')),
      minDate: this.mget('min_date') != null ? new Date(this.mget('min_date')) : null,
      maxDate: this.mget('max_date') != null ? new Date(this.mget('max_date')) : null,
      onSelect: this.onSelect
    });
    this.$el.append([$label, $datepicker]);
    return this;
  };

  DatePickerView.prototype.onSelect = function(dateText, ui) {
    var ref;
    this.mset('value', new Date(dateText));
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return DatePickerView;

})(ContinuumView);

DatePicker = (function(superClass) {
  extend(DatePicker, superClass);

  function DatePicker() {
    return DatePicker.__super__.constructor.apply(this, arguments);
  }

  DatePicker.prototype.type = "DatePicker";

  DatePicker.prototype.default_view = DatePickerView;

  DatePicker.prototype.defaults = function() {
    return _.extend({}, DatePicker.__super__.defaults.call(this), {
      value: Date.now(),
      min_date: null,
      max_date: null
    });
  };

  return DatePicker;

})(InputWidget.Model);

module.exports = {
  Model: DatePicker,
  View: DatePickerView
};
