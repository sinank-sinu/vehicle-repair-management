/** @odoo-module */
import { renderToElement } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";
publicWidget.registry.get_top_repairs = publicWidget.Widget.extend({
   selector : '.top_repairs',
    async willStart() {
       const result = await rpc('/repairs', {});
           console.log("------------------------nokkada muthee-----------------------")

       if(result){
           this.$target.empty().html(renderToElement('vehicle_repair_management.category_data', {result: result}))
       }
   },
});

