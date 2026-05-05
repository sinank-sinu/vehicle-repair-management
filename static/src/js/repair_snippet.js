/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.TopRepairsSnippet = publicWidget.Widget.extend({
    selector: '.s_top_repairs_dynamic',
    start: function () {
        jsonrpc('/repair/get_top_services', {}).then((data) => {
            let html = '<div class="row">';
            data.forEach(repair => {
                html += `<div class="col-3">
                            <a href="/repair/details/${repair.id}">
                                <h5>${repair.name}</h5>
                                <p>Cost: ${repair.total_parts_labor_cost}</p>
                            </a>
                         </div>`;
            });
            html += '</div>';
            this.$el.find('.dynamic_content_area').html(html);
        });
    },
});
