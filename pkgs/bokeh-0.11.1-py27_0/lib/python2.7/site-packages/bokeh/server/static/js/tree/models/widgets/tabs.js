var $, $1, ContinuumView, Tabs, TabsView, Widget, _, build_views, tabs_template,
  extend = function(child, parent) { for (var key in parent) { if (hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
  hasProp = {}.hasOwnProperty;

_ = require("underscore");

$ = require("jquery");

$1 = require("bootstrap/tab");

build_views = require("../../common/build_views");

ContinuumView = require("../../common/continuum_view");

tabs_template = require("./tabs_template");

Widget = require("./widget");

TabsView = (function(superClass) {
  extend(TabsView, superClass);

  function TabsView() {
    return TabsView.__super__.constructor.apply(this, arguments);
  }

  TabsView.prototype.initialize = function(options) {
    TabsView.__super__.initialize.call(this, options);
    this.views = {};
    this.render();
    return this.listenTo(this.model, 'change', this.render);
  };

  TabsView.prototype.render = function() {
    var $panels, active, child, children, html, j, key, len, panel, ref, ref1, ref2, tab, tabs, that, val;
    ref = this.views;
    for (key in ref) {
      if (!hasProp.call(ref, key)) continue;
      val = ref[key];
      val.$el.detach();
    }
    this.$el.empty();
    tabs = this.mget('tabs');
    active = this.mget("active");
    children = (function() {
      var j, len, results;
      results = [];
      for (j = 0, len = tabs.length; j < len; j++) {
        tab = tabs[j];
        results.push(tab.get("child"));
      }
      return results;
    })();
    build_views(this.views, children);
    html = $(tabs_template({
      tabs: tabs,
      active: function(i) {
        if (i === active) {
          return 'bk-bs-active';
        } else {
          return '';
        }
      }
    }));
    that = this;
    html.find("> li > a").click(function(event) {
      var panelId, panelIdx, ref1;
      event.preventDefault();
      $(this).tab('show');
      panelId = $(this).attr('href').replace('#tab-', '');
      tabs = that.model.get('tabs');
      panelIdx = _.indexOf(tabs, _.find(tabs, function(panel) {
        return panel.id === panelId;
      }));
      that.model.set('active', panelIdx);
      return (ref1 = that.model.get('callback')) != null ? ref1.execute(that.model) : void 0;
    });
    $panels = html.children(".bk-bs-tab-pane");
    ref1 = _.zip(children, $panels);
    for (j = 0, len = ref1.length; j < len; j++) {
      ref2 = ref1[j], child = ref2[0], panel = ref2[1];
      $(panel).html(this.views[child.id].$el);
    }
    this.$el.append(html);
    this.$el.tabs;
    return this;
  };

  return TabsView;

})(ContinuumView);

Tabs = (function(superClass) {
  extend(Tabs, superClass);

  function Tabs() {
    return Tabs.__super__.constructor.apply(this, arguments);
  }

  Tabs.prototype.type = "Tabs";

  Tabs.prototype.default_view = TabsView;

  Tabs.prototype.defaults = function() {
    return _.extend({}, Tabs.__super__.defaults.call(this), {
      tabs: [],
      active: 0,
      callback: null
    });
  };

  return Tabs;

})(Widget.Model);

module.exports = {
  Model: Tabs,
  View: TabsView
};
