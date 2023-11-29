<template>
    <b-container fluid>
        <b-row>
            <b-col lg="4" class="my-1 mb-3">
                <b-form-group label="Filter" label-for="filter-input" label-cols-sm="3" label-align-sm="right"
                    label-size="sm" class="mb-0">
                    <b-input-group size="sm">
                        <b-form-input id="filter-input" v-model="filter" type="search"
                            placeholder="Type to Search"></b-form-input>

                        <b-input-group-append>
                            <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
            <!-- <b-col lg="4" class="my-1 mb-3">
                <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="5" align="fill" size="sm"
                    class="my-0"></b-pagination>
            </b-col> -->
            <b-col v-if="user_role == 'admin'" lg="4" class="my-1 mb-3 d-flex justify-content-end">
                <b-button @click="exportStactCSV">Export CSV</b-button>
            </b-col>


            <b-table bordered :busy="isBusy" :items="bills" :fields="fields" :filter="filter" :current-page="currentPage"
                stacked="md" show-empty small>

                <template #table-busy>
                    <div class="text-center text-secondary my-2">
                        <b-spinner type="grow" class="align-middle"></b-spinner>
                        <strong class="ml-2">Loading...</strong>
                    </div>
                </template>

                <template #cell(name)="row">
                    {{ row.value.first }} {{ row.value.last }}
                </template>

                <template #cell(billImg)="row">
                    <b-button size="sm" @click="billInfo(row.item, row.index, $event.target)" class="mr-1">
                        View Bill
                    </b-button>
                </template>

                <template #cell(voucherImg)="row">
                    <b-button size="sm" @click="voucherInfo(row.item, row.index, $event.target)" class="mr-1">
                        View Voucher
                    </b-button>
                </template>

                <template v-if="bill_type == 'pending'" #cell(actions)="row">
                    <div>
                        <b-button variant="success" size="sm" @click="verifyBill(row.item, row.index, $event.target)"
                            class="mr-1">
                            Verify Bill
                        </b-button>
                        <b-button variant="danger" size="sm" @click="rejectBill(row.item, row.index, $event.target)"
                            class="mr-1">
                            Reject Bill
                        </b-button>
                        <b-button class="m-1" variant="warning" size="sm" @click="row.toggleDetails">
                            {{ row.detailsShowing ? 'Hide' : 'Show' }} View Full Bill
                        </b-button>
                    </div>
                </template>

                <template v-if="bill_type == 'all-pending' || bill_type == 'verified'" #cell(coreActions)="row">
                    <div>
                        <b-button class="m-1" variant="warning" size="sm" @click="row.toggleDetails">
                            {{ row.detailsShowing ? 'Hide' : 'Show' }} View Full Bill
                        </b-button>
                    </div>
                </template>

                <template #row-details="row">
                    <b-card class="view-bill-card">
                        <table border="solid">
                            <tr>
                                <td>Bill Number</td>
                                <td>{{ row.item.bill_number }}</td>
                            </tr>
                            <tr>
                                <td>Account Holder Name</td>
                                <td>{{ row.item.acc_holder_name }}</td>
                            </tr>
                            <tr>
                                <td>Account Number</td>
                                <td>{{ row.item.acc_number }}</td>
                            </tr>
                            <tr>
                                <td>Bill Amount</td>
                                <td>{{ row.item.bill_amount }}</td>
                            </tr>
                            <tr>
                                <td>Bill Amount in Words</td>
                                <td>{{ row.item.bill_amount_in_words }}</td>
                            </tr>
                            <tr>
                                <td>Bank Name</td>
                                <td>{{ row.item.bank_name }}</td>
                            </tr>
                            <tr>
                                <td>Bank Branch</td>
                                <td>{{ row.item.bank_branch }}</td>
                            </tr>
                            <tr>
                                <td>IFSC Code</td>
                                <td>{{ row.item.ifsc_code }}</td>
                            </tr>
                            <tr>
                                <td>Bill Description</td>
                                <td>{{ row.item.bill_description }}</td>
                            </tr>
                        </table>
                    </b-card>
                </template>

                <template #cell(adminAction)="row">
                    <div>
                        <b-button variant="success" size="sm" @click="processBill(row.item, row.index, $event.target)">
                            Processed
                        </b-button>
                    </div>
                </template>
            </b-table>

            <b-button v-if="bill_type == 'generate-eas-sr' && !isBusy" variant="primary" size="sm" @click="generateEasSr"
                class="mr-1">
                Generate SR EAS
            </b-button>

            <!-- Bill Info modal -->
            <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
                <pre>
                <a v-bind:href="infoModal.content" target="_blank">
                    <b-button variant="primary">Download Bill</b-button>
                </a>
            </pre>
            </b-modal>

            <!-- Voucher Info modal -->
            <b-modal :id="voucherInfoModal.id" :title="voucherInfoModal.title" ok-only @hide="resetVoucherInfoModal">
                <pre>
                <a v-bind:href="voucherInfoModal.content" target="_blank">
                    <b-button variant="primary">Download Voucher</b-button>
                </a>
                </pre>
            </b-modal>

            <!-- Verify modal -->
            <b-modal id="verify-modal" ref="modal" title="Confirm Bill Verification" @show="resetModal" @hidden="resetModal"
                @ok="handleOk">
                <form ref="form" @submit.stop.prevent="handleSubmit">
                    <b-form-group label="Confirm" label-for="confirm-input" invalid-feedback="Confirmation is required"
                        description="Type confirm" :state="confirmState">
                        <b-form-input autocomplete="off" id="confirm-input" v-model="confirm" :state="confirmState"
                            required></b-form-input>
                    </b-form-group>
                </form>
            </b-modal>

            <!-- Reject modal -->
            <b-modal id="reject-modal" ref="modal" title="Confirm Bill Rejection" @show="resetModal" @hidden="resetModal"
                @ok="handleRejectOk">
                <form ref="form" @submit.stop.prevent="handleReject">
                    <b-form-group label="Reason" label-for="reason-input" invalid-feedback="Reason is required"
                        description="Type reason" :state="reasonState">
                        <b-form-input autocomplete="off" id="reason-input" v-model="rejectReason" :state="reasonState"
                            required></b-form-input>
                    </b-form-group>
                    <b-form-group label="Confirm" label-for="confirm-input" invalid-feedback="Confirmation is required"
                        description="Type confirm" :state="confirmState">
                        <b-form-input autocomplete="off" id="confirm-input" v-model="confirm" :state="confirmState"
                            required></b-form-input>
                    </b-form-group>
                </form>
            </b-modal>

            <!-- Processed modal -->
            <b-modal id="processed-modal" ref="modal" title="Confirm Action" @show="resetModal" @hidden="resetModal"
                @ok="handleRejectOk">
                <form ref="form" @submit.stop.prevent="handleReject">
                    <b-form-group label="Confirm" label-for="confirm-input" invalid-feedback="Confirmation is required"
                        description="Type confirm" :state="confirmState">
                        <b-form-input autocomplete="off" id="confirm-input" v-model="confirm" :state="confirmState"
                            required></b-form-input>
                    </b-form-group>
                </form>
            </b-modal>
        </b-row>
    </b-container>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';
import config from '@/config.js'
import exportFromJSON from "export-from-json";

export default {
    name: 'BillTable',
    props: ['bill_type'],
    data() {
        return {
            confirm: '',
            confirmState: null,
            isBusy: true,
            bills: [],
            totalRows: 1,
            currentPage: 1,
            filter: null,
            infoModal: {
                id: 'info-modal',
                title: '',
                content: ''
            },
            voucherInfoModal: {
                id: 'voucher-info-modal',
                title: '',
                content: ''
            },
            verifyId: null,
            user_role: null,
            rejectReason: '',
            reasonState: null,
            tempRejectBillData: {
                temp_bill_number: null,
                temp_bill_description: null,
                temp_poc_email: null,
            },
        }
    },
    computed: {
        fields() {
            if (this.bill_type == 'pending') {
                return [
                    { key: 'bill_number', label: 'Bill Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_status', label: 'Bill Status', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                    { key: 'actions', label: 'Actions' },
                ]
            } else if (this.bill_type == "verified" && this.user_role == "Super Coordinator") {
                return [
                    { key: 'voucher', label: 'Voucher Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'voucher_generated_on', label: 'Voucher Date', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'voucherImg', label: 'Voucher Image', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                ]
            } else if (this.bill_type == "verified" && this.user_role == "Core") {
                return [
                    { key: 'voucher', label: 'Voucher Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'voucher_generated_on', label: 'Voucher Date', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'stact_processed', lable: 'Bill Status', sortable: true },
                    { key: 'voucherImg', label: 'Voucher Image', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                    { key: 'coreActions', label: 'Actions' },
                ]
            } else if (this.bill_type == "all-pending" && this.user_role == "Core") {
                return [
                    { key: 'bill_number', label: 'Bill Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_status', label: 'Bill Status', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                    { key: 'coreActions', label: 'Actions' },
                ]
            } else if (this.bill_type == 'generate-eas-sr' && this.user_role == 'Core') {
                return [
                    { key: 'bill_number', label: 'Bill Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_status', label: 'Bill Status', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                ]
            } else if (this.bill_type == 'eas-generated' && this.user_role == 'Core') {
                return [
                    { key: 'bill_number', label: 'Bill Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'poc_name', label: 'POC Name', sortable: true },
                    { key: 'poc_email', label: 'POC Email', sortable: true },
                    { key: 'poc_phone', label: 'POC Phone', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_status', label: 'Bill Status', sortable: true },
                    { key: 'billImg', label: 'Bill Image' },
                ]
            } else if (this.bill_type == 'approved' && this.user_role == 'admin') {
                return [
                    { key: 'voucher', label: 'Voucher Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_number', label: 'Bill Number', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_description', label: 'Bill Description', sortable: true },
                    { key: 'vendor_name', label: 'Vendor Name', sortable: true },
                    { key: 'acc_number', label: 'Vendor Account Number', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'voucherImg', label: 'Voucher Image', sortable: true },
                    { key: 'billImg', label: 'Bill Image', sortable: true },
                    { key: 'adminAction', label: 'Action' }
                ]
            } else if (this.bill_type == 'processed' && (this.user_role == 'admin' || this.user_role == 'pod-admin')) {
                return [
                    { key: 'voucher', label: 'Voucher Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'voucher_generated_on', label: 'Voucher Date', sortable: true },
                    { key: 'bill_description', label: 'Bill Description', sortable: true },
                    { key: 'vendor_name', label: 'Vendor Name', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'stact_processed_on', label: 'Stact Processed On', sortable: true },
                    { key: 'voucherImg', label: 'Voucher Image', sortable: true },
                ]
            } else if (this.bill_type == 'approved' && this.user_role == 'pod-admin') {
                return [
                    { key: 'voucher', label: 'Voucher Number', sortable: true, sortDirection: 'desc' },
                    { key: 'bill_number', label: 'Bill Number', sortable: true },
                    { key: 'bill_date', label: 'Bill Date', sortable: true },
                    { key: 'bill_type', label: 'Bill Type', sortable: true },
                    { key: 'bill_department', label: 'Department', sortable: true },
                    { key: 'bill_description', label: 'Bill Description', sortable: true },
                    { key: 'vendor_name', label: 'Vendor Name', sortable: true },
                    { key: 'acc_number', label: 'Vendor Account Number', sortable: true },
                    { key: 'gst_number', label: 'GST Number', sortable: true },
                    { key: 'bill_amount', label: 'Bill Amount', sortable: true },
                    { key: 'voucherImg', label: 'Voucher Image', sortable: true },
                    { key: 'billImg', label: 'Bill Image', sortable: true },
                ]
            } else {
                return null
            }
        }
    },
    methods: {
        ...mapActions(['setBillId']),
        exportStactCSV() {
            const bills = JSON.parse(JSON.stringify(this.bills));
            if (!bills) return;
            try {
                const data = bills.map((item) => {
                    return {
                        "Bill Number": item.bill_number,
                        "Bill Date": item.bill_date,
                        "Bill Type": item.bill_type,
                        "Bill Department": item.bill_department,
                        "Bill Description": item.bill_description,
                        "POC Name": item.poc_name,
                        "POC Phone": item.poc_phone,
                        "Vendor Name": item.vendor_name,
                        "Vendor Address": item.vendor_address,
                        "Bank Account Number": parseInt(item.acc_number),
                        "Bank Name": item.bank_name,
                        "Account Holder Name": item.acc_holder_name,
                        "IFSC Code": item.ifsc_code,
                        "Payment Type": item.bill_type,
                        "GST Number": item.gst_number,
                        "Bill Amount": item.bill_amount,
                        "Bill Amount in Words": item.bill_amount_in_words,
                        "Voucher Number": item.voucher,
                        "Voucher Date": item.voucher_generated_on,
                    };
                });
                const fileName = "exported-data";
                const exportType = exportFromJSON.types["csv"];
                exportFromJSON({ data, fileName, exportType });
            } catch (e) {
                throw new Error("Parsing failed!");
            }
        },
        async billInfo(item, index, button) {
            var formData = new FormData()
            formData.append('bill_id', item.id)
            await axios.post(`${config.API_BASE_URL}/bills/get-bill-view-url`, formData, {
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                }
            })
                .then(response => {
                    this.infoModal.title = `Bill Number: ${item.bill_number}`
                    this.infoModal.content = response.data.bill_url
                    this.$root.$emit('bv::show::modal', this.infoModal.id, button)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async voucherInfo(item, index, button) {
            var formData = new FormData()
            formData.append('bill_id', item.id)
            await axios.post(`${config.API_BASE_URL}/bills/get-voucher-view-url`, formData, {
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                }
            })
                .then(response => {
                    this.voucherInfoModal.title = `Voucher Number: ${item.voucher}`
                    this.voucherInfoModal.content = response.data.voucher_url
                    this.$root.$emit('bv::show::modal', this.voucherInfoModal.id, button)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        verifyBill(item, button) {
            this.verifyId = item.id
            this.setBillId(this.verifyId)
            this.$root.$emit('bv::show::modal', 'verify-modal', button)
        },
        rejectBill(item, button) {
            this.verifyId = item.id
            this.setBillId(this.verifyId)
            this.tempRejectBillData.temp_bill_number = item.bill_number
            this.tempRejectBillData.temp_bill_description = item.bill_description
            this.tempRejectBillData.temp_poc_email = item.poc_email
            this.$root.$emit('bv::show::modal', 'reject-modal', button)
        },
        processBill(item, button) {
            this.verifyId = item.id
            this.setBillId(this.verifyId)
            this.$root.$emit('bv::show::modal', 'processed-modal', button)
        },
        resetInfoModal() {
            this.infoModal.title = ''
            this.infoModal.content = ''
        },
        resetVoucherInfoModal() {
            this.voucherInfoModal.title = ''
            this.voucherInfoModal.content = ''
        },
        onFiltered(filteredItems) {
            // Trigger pagination to update the number of buttons/pages due to filtering
            this.totalRows = filteredItems.length
            this.currentPage = 1
        },
        resetModal() {
            this.confirm = '',
                this.reject = '',
                this.confirmState = null,
                this.rejectState = null
        },
        handleOk(bvModalEvent) {
            // Prevent modal from closing
            bvModalEvent.preventDefault()
            // Trigger submit handler
            this.handleSubmit()
        },
        handleRejectOk(bvModalEvent) {
            // Prevent modal from closing
            bvModalEvent.preventDefault()
            // Trigger submit handler
            this.handleReject()
        },
        async handleReject() {
            if (!this.confirmState && !this.rejectState) {
                return
            }
            var formData = new FormData();
            formData.append('bill_id', this.verifyId);


            var emailFormData = new FormData();
            emailFormData.append('bill_number', this.tempRejectBillData.temp_bill_number);
            emailFormData.append('bill_description', this.tempRejectBillData.temp_bill_description);
            emailFormData.append('email', this.tempRejectBillData.temp_poc_email);
            emailFormData.append('remarks', this.rejectReason);

            if (this.user_role == 'admin') {
                await axios.put(`${config.API_BASE_URL}/bills/stact-process-bill`, formData, {
                    headers: {
                        'x-access-token': localStorage.getItem('token')
                    }
                })
                    .then(() => {
                        this.$bvToast.toast(`Bill processed successfully`, {
                            title: 'Bill Processed',
                            variant: 'success',
                            solid: true
                        })
                        this.getAllStactBills()
                        this.verifyId = null
                        this.$nextTick(() => {
                            this.resetModal()
                            this.$bvModal.hide('processed-modal')
                        })
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }

            if (this.user_role == 'Core' || this.user_role == 'Super Coordinator') {
                await axios.post(`${config.API_BASE_URL}/send-reject-mail`, emailFormData, {
                    headers: {
                        'x-access-token': localStorage.getItem('token'),
                    }
                }).then(async () => {
                    this.tempRejectBillData.temp_bill_number = null
                    this.tempRejectBillData.temp_bill_description = null
                    this.tempRejectBillData.temp_poc_email = null
                    await axios.put(`${config.API_BASE_URL}/bills/reject`, formData,
                        {
                            headers: {
                                'x-access-token': localStorage.getItem('token')
                            }
                        })
                        .then(() => {
                            this.$bvToast.toast(`Bill rejected successfully`, {
                                title: 'Bill Rejection',
                                variant: 'danger',
                                solid: true
                            })
                            if (this.user_role == 'Core') {
                                this.getAllScApprovedBills();
                            }
                            if (this.user_role == 'Super Coordinator') {
                                this.getPendingBills();
                            }
                            this.verifyId = null
                            this.$nextTick(() => {
                                this.resetModal()
                                this.$bvModal.hide('reject-modal')
                            })
                        })
                        .catch(error => {
                            console.log(error)
                        })
                }).catch(error => {
                    console.log(error)
                })
            }
        },
        handleSubmit() {
            // Exit when the form isn't valid
            if (!this.confirmState) {
                return
            }
            // Push the name to submitted names
            // this.submittedNames.push(this.name)
            // Hide the modal manually
            var formData = new FormData();
            formData.append('bill_id', this.verifyId);
            if (this.user_role == 'Super Coordinator') {

                axios.put(`${config.API_BASE_URL}/bills/sc-approved`, formData,
                    {
                        headers: {
                            'x-access-token': localStorage.getItem('token')
                        }
                    })
                    .then(() => {
                        this.$bvToast.toast(`Bill verified successfully`, {
                            title: 'Bill Verification',
                            variant: 'success',
                            solid: true
                        })
                        if (this.user_role == 'Super Coordinator') {
                            this.getPendingBills();
                        }
                        if (this.user_role == 'Core') {
                            this.getAllScApprovedBills();
                        }
                        this.verifyId = null
                        this.$nextTick(() => {
                            this.$bvModal.hide('verify-modal')
                        })
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            }
            else if (this.user_role == 'Core') {
                this.$router.push({ name: 'voucher' })
            }
        },

        async getPendingBills() {
            await axios.get(`${config.API_BASE_URL}/pending-bills`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllPendingBills() {
            await axios.get(`${config.API_BASE_URL}/bills/all-pending-bills`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getScApprovedBills() {
            await axios.get(`${config.API_BASE_URL}/bills/sc-fc-approved`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllScApprovedBills() {
            await axios.get(`${config.API_BASE_URL}/bills/sc-approved-all`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getFcApprovedBills() {
            await axios.get(`${config.API_BASE_URL}/bills/fc-approved`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllSrPendingBills() {
            await axios.get(`${config.API_BASE_URL}/bills/sr-pending`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllStactBills() {
            await axios.get(`${config.API_BASE_URL}/bills/stact-pending`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllStactProcessedBills() {
            await axios.get(`${config.API_BASE_URL}/bills/stact-processed`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async assignUserRole() {
            await axios.get(`${config.API_BASE_URL}/user`, {
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                },
            }).then((res) => {
                this.user_role = res.data.role;
                // console.log('user role: ', this.user_role)
            }).catch((err) => {
                console.log(err);
            });
        },

        async generateEasSr() {
            await axios.get(`${config.API_BASE_URL}/generate-eas-sr`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then(() => {
                    this.$bvToast.toast(`EAS generated successfully`, {
                        title: 'EAS Generation',
                        variant: 'success',
                        solid: true
                    })
                    this.getAllSrPendingBills();
                })
                .catch((error) => {
                    console.log(error);
                });
        },

        async getAllEasGeneratedBills() {
            await axios.get(`${config.API_BASE_URL}/bills/eas-generated`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            })
                .then((response) => {
                    this.bills = response.data.bills;
                    this.isBusy = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
    },
    watch: {
        confirm(newVal) {
            if (newVal === '') {
                this.confirmState = null
            } else if (newVal === 'confirm') {
                this.confirmState = true
            } else {
                this.confirmState = false
            }
        },
        rejectReason(newVal) {
            if (newVal === '') {
                this.rejectState = null
            } else if (newVal > 0) {
                this.rejectState = true
            } else {
                this.rejectState = false
            }
        },
    },
    async created() {
        // console.log('bill type: ', this.bill_type)
        // Set the initial number of items
        await this.assignUserRole();
        this.totalRows = this.bills.length
        if (this.bill_type == 'pending' && this.user_role == 'Super Coordinator') {
            await this.getPendingBills();
        }

        else if (this.bill_type == 'verified' && this.user_role == 'Super Coordinator') {
            await this.getScApprovedBills();
            // await this.getFcApprovedBills();
        }

        else if (this.bill_type == 'pending' && this.user_role == 'Core') {
            await this.getAllScApprovedBills();
        }

        else if (this.bill_type == 'verified' && this.user_role == 'Core') {
            await this.getFcApprovedBills();
        }

        else if (this.bill_type == 'all-pending' && this.user_role == 'Core') {
            await this.getAllPendingBills();
        }

        else if (this.bill_type == 'generate-eas-sr' && this.user_role == 'Core') {
            await this.getAllSrPendingBills();
        }

        else if (this.bill_type == 'eas-generated' && this.user_role == 'Core') {
            await this.getAllEasGeneratedBills();
        }

        else if (this.bill_type == 'approved' && (this.user_role == 'admin' || this.user_role == 'pod-admin')) {
            await this.getAllStactBills();
        }

        else if (this.bill_type == 'processed' && (this.user_role == 'admin' || this.user_role == 'pod-admin')) {
            await this.getAllStactProcessedBills()
        }

        else {
            await this.getAllScApprovedBills();
        }
    },
}
</script>

<style scoped>
.view-bill-card {
    margin: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 0 10px #ccc;
    display: flex;
    align-items: center;
    background-color: #fafafa;
}
</style>