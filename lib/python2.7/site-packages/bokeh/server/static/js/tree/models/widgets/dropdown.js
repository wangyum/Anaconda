var $, AbstractButton, ContinuumView, Dropdown, DropdownView, _,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

ContinuumView = require("../../common/continuum_view");

AbstractButton = require("./abstract_button");

DropdownView = (function(superClass) {
  extend(DropdownView, superClass);

  function DropdownView() {
    return DropdownView.__super__.constructor.apply(this, arguments);
  }

  DropdownView.prototype.tagName = "div";

  DropdownView.prototype.initialize = function(options) {
    DropdownView.__super__.initialize.call(this, options);
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  DropdownView.prototype.render = function() {
    var $a, $button, $caret, $divider, $item, $menu, $toggle, i, item, label, len, ref, split, that, value;
    this.$el.empty();
    split = this.mget("default_value") != null;
    $button = $('<button></button>');
    $button.addClass("bk-bs-btn");
    $button.addClass("bk-bs-btn-" + this.mget("type"));
    $button.text(this.mget("label"));
    $caret = $('<span class="bk-bs-caret"></span>');
    if (!split) {
      $button.addClass("bk-bs-dropdown-toggle");
      $button.attr("data-bk-bs-toggle", "dropdown");
      $button.append(document.createTextNode(" "));
      $button.append($caret);
      $toggle = $('');
    } else {
      $button.click((function(_this) {
        return function() {
          return _this.change_input(_this.mget("default_value"));
        };
      })(this));
      $toggle = $('<button></button>');
      $toggle.addClass("bk-bs-btn");
      $toggle.addClass("bk-bs-btn-" + this.mget("type"));
      $toggle.addClass("bk-bs-dropdown-toggle");
      $toggle.attr("data-bk-bs-toggle", "dropdown");
      $toggle.append($caret);
    }
    $menu = $('<ul class="bk-bs-dropdown-menu"></ul>');
    $divider = $('<li class="bk-bs-divider"></li>');
    ref = this.mget("menu");
    for (i = 0, len = ref.length; i < len; i++) {
      item = ref[i];
      $item = item != null ? ((label = item[0], value = item[1], item), $a = $('<a></a>').text(label).data('value', value), that = this, $a.click(function(e) {
        return that.change_input($(this).data('value'));
      }), $('<li></li>').append($a)) : $divider;
      $menu.append($item);
    }
    this.$el.addClass("bk-bs-btn-group");
    this.$el.append([$button, $toggle, $menu]);
    return this;
  };

  DropdownView.prototype.change_input = function(value) {
    var ref;
    this.mset('value', value);
    return (ref = this.mget('callback')) != null ? ref.execute(this.model) : void 0;
  };

  return DropdownView;

})(ContinuumView);

Dropdown = (function(superClass) {
  extend(Dropdown, superClass);

  function Dropdown() {
    return Dropdown.__super__.constructor.apply(this, arguments);
  }

  Dropdown.prototype.type = "Dropdown";

  Dropdown.prototype.default_view = DropdownView;

  Dropdown.prototype.defaults = function() {
    return _.extend({}, Dropdown.__super__.defaults.call(this), {
      value: null,
      default_value: null,
      label: "Dropdown",
      menu: []
    });
  };

  return Dropdown;

})(AbstractButton.Model);

module.exports = {
  Model: Dropdown,
  View: DropdownView
};
