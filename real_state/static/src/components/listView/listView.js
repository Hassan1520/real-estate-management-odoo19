/* @odoo-module */

import {Component, useState, onWillUnmount} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {rpc} from "@web/core/network/rpc"; // استيراد مباشر
import {FormView} from "@real_state/components/formView/formView"; // استيراد مباشر

export class ListViewAction extends Component {
    static template = "real_state.ListView";
    static components = {FormView};
    setup() {
        this.state = useState({
            'records': []
        });

        this.orm = useService("orm");
        this.rpc = rpc;
        this.loadRecord()
        this.intervalId = setInterval(() => {
            this.loadRecord()
        }, 2000);

        this.onRecordCreated = this.onRecordCreated.bind(this);

        onWillUnmount(() => {
            clearInterval(this.intervalId)
        });

    };

    // async loadRecord() {
    //     const result = await this.orm.searchRead(
    //         "property",
    //     [],
    //     ["id", "name", "postcode", "date_availability"],
    //     { limit: 100 });
    //     this.state.records = result;
    // };

    async loadRecord() {
        const result = await this.rpc("/web/dataset/call_kw", {
            model: 'property',
            method: 'search_read',
            args: [[]],
            kwargs: {fields: ["id", "name", "postcode", "date_availability"]},
        });
        console.log(result)
        this.state.records = result;
    };

    async createRecord() {
        await this.rpc("/web/dataset/call_kw", {
            model: 'property',
            method: 'create',
            args: [{
                name: "New prop method",
                postcode: "123456",
            }],
            kwargs: {},
        });
        this.loadRecord();
    };
    async deleteRecord(recordId) {
        await this.rpc("/web/dataset/call_kw", {
            model: 'property',
            method: 'unlink',
            args: [recordId],
            kwargs: {},
        });
        this.loadRecord();
    };
    toggleCreateForm(){
      this.state.showCreateForm = !this.state.showCreateForm;
    }
    onRecordCreated(){
        this.loadRecord();
        this.state.showCreateForm = false;
    }
}

registry.category("actions").add("real_state.action_list_view", ListViewAction);