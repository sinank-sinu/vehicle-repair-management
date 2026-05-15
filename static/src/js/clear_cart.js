/** @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.ClearCartWidget = publicWidget.Widget.extend(
    {
    selector: '.oe_website_sale',
    events: {
        'click .js_clear_cart': 'ClearCart',        
    },

    async ClearCart() {
        await rpc('/shop/clear_cart', {});
          window.location.reload();
    },
}
);
