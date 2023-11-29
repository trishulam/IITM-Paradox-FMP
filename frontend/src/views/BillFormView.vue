<template>
    <b-container fluid>
        <b-card title="Paradox 2023 Bill Submission" style="margin: 2rem auto;">
            <b-form style="margin: 0 auto" @submit="onSubmit">
                <b-button class="mt-1" variant="warning">
                    <a target="_blank" style="color: black; text-decoration: none;"
                        href="https://docs.google.com/document/d/16vvWfcO8y9LsWGhNRjiV8eOAECkai4f9O3qB9RLKY5M/edit?usp=sharing">
                        Download Finance SOP
                    </a>
                </b-button>
                <b-row>
                    <!-- <div class="d-flex justify-content-around"> -->
                    <b-col cols="12" lg="6" class="d-flex justify-content-center">
                        <div class="poc-info-card">
                            <b-card class="mt-3" header="POC Contact Information">
                                <div class="text-left" role="group">
                                    <b-row>
                                        <b-col cols="12" md="6">
                                            <b-form-group>
                                                <label for="input-poc-name">Name:</label>
                                                <b-form-input id="input-poc-name" v-model="pocName" required
                                                    :state="pocNameState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter your name" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid name
                                                </b-form-invalid-feedback>
                                            </b-form-group>

                                            <b-form-group>
                                                <label class="mt-2" for="input-department">Department/Event:</label>
                                                <b-form-select required v-model="departmentCategory"
                                                    :options="departmentOptions"></b-form-select>
                                            </b-form-group>
                                        </b-col>
                                        <b-col cols="12" md="6">
                                            <b-form-group>
                                                <label for="input-event-name">Event Name:</label>
                                                <b-form-input id="input-event-name" v-model="eventName"
                                                    :state="eventNameState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter Event Name" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid event name
                                                </b-form-invalid-feedback>
                                            </b-form-group>

                                            <b-form-group>
                                                <label class="mt-2" for="input-phone">Phone Number:</label>
                                                <b-form-input id="input-phone" v-model="pocPhone" required
                                                    :state="pocPhoneState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter your Phone Number" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid phone number
                                                </b-form-invalid-feedback>
                                            </b-form-group>
                                        </b-col>
                                    </b-row>
                                </div>
                            </b-card>

                            <b-card v-if="billType == 'Vendor Payment'" class="mt-5" header="Vendor Bank Details">
                                <div class="text-left" role="group">
                                    <b-row>
                                        <b-col cols="12" md="6">
                                            <b-form-group>
                                                <label for="input-poc-name">Account Holder Name:</label>
                                                <b-form-input id="input-acc-holder-name" v-model="accHolderName" required
                                                    :state="accHolderNameState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter account holder name" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid name
                                                </b-form-invalid-feedback>
                                            </b-form-group>

                                            <b-form-group>
                                                <label for="input-acc-number">Account Number:</label>
                                                <b-form-input id="input-acc-number" v-model="accNumber" required
                                                    :state="accNumberState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter account number" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid account number
                                                </b-form-invalid-feedback>
                                            </b-form-group>
                                        </b-col>
                                        <b-col cols="12" md="6">
                                            <b-form-group>
                                                <label for="input-bank-name">Bank Name:</label>
                                                <b-form-input id="input-bank-name" v-model="bankName" required
                                                    :state="bankNameState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter bank name" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid bank name
                                                </b-form-invalid-feedback>
                                            </b-form-group>

                                            <b-form-group>
                                                <label for="input-ifsc">IFSC Code:</label>
                                                <b-form-input id="input-ifsc" v-model="ifscCode" required
                                                    :state="ifscCodeState"
                                                    aria-describedby="input-live-help input-live-feedback"
                                                    placeholder="Enter IFSC Code" trim></b-form-input>

                                                <!-- This will only be shown if the preceding input has an invalid state -->
                                                <b-form-invalid-feedback id="input-live-feedback">
                                                    Enter a valid ifsc code
                                                </b-form-invalid-feedback>
                                            </b-form-group>
                                        </b-col>
                                    </b-row>
                                    <b-row class="d-flex justify-content-center">
                                        <b-form-group>
                                            <label for="input-bank-branch">Branch Name:</label>
                                            <b-form-input id="input-bank-branch" v-model="branchName" required
                                                aria-describedby="input-live-help input-live-feedback"
                                                placeholder="Enter bank branch" trim></b-form-input>
                                        </b-form-group>
                                    </b-row>
                                </div>
                            </b-card>
                        </div>
                    </b-col>

                    <b-col cols="12" lg="6" class="d-flex justify-content-center">
                        <div class="bill-details-card">
                            <b-card class="mt-3" header="Bill Details">
                                <div class="text-left" role="group">
                                    <label for="input-bill-number">Bill Number:</label>
                                    <b-form-input id="input-bill-number" v-model="billNumber" required
                                        aria-describedby="input-live-help input-live-feedback"
                                        placeholder="Enter the Bill Number" trim></b-form-input>

                                    <b-form-group>
                                        <label class="mt-2" for="bill-datepicker">Date of Bill</label>
                                        <b-form-datepicker required id="bill-datepicker"
                                            v-model="billDate"></b-form-datepicker>
                                    </b-form-group>

                                    <b-form-group class="mt-2" label="Type of Bill" v-slot="{ ariaDescribedby }">
                                        <b-form-radio-group id="radio-group-2" v-model="billType"
                                            :aria-describedby="ariaDescribedby" name="radio-sub-component" required>
                                            <b-form-radio value="Vendor Payment">Vendor Payment</b-form-radio>
                                            <b-form-radio value="Student Reimbursement">Student
                                                Reimbursement</b-form-radio>
                                        </b-form-radio-group>
                                    </b-form-group>

                                    <b-form-group>
                                        <label for="input-vendor-name" class="mt-2">Vendor Name:</label>
                                        <b-form-input id="input-vendor-name" v-model="vendorName" required
                                            :state="vendorNameState" aria-describedby="input-live-help input-live-feedback"
                                            placeholder="Enter the vendor name" trim></b-form-input>

                                        <!-- This will only be shown if the preceding input has an invalid state -->
                                        <b-form-invalid-feedback id="input-live-feedback">
                                            Enter a valid name
                                        </b-form-invalid-feedback>
                                    </b-form-group>

                                    <b-form-group>
                                        <label for="input-vendor-address" class="mt-2">Vendor Address:</label>
                                        <b-form-textarea id="textarea" v-model="vendorAddress" required
                                            placeholder="Enter Vendor Address" rows="3" max-rows="6"></b-form-textarea>
                                    </b-form-group>

                                    <b-form-group class="mt-2" label="Type of Payment" v-slot="{ ariaDescribedby }">
                                        <b-form-radio-group id="radio-group-3" v-model="billPaymentType"
                                            :aria-describedby="ariaDescribedby" name="radio-sub-component-2" required>
                                            <b-form-radio :disabled="isAdvancePaymentDisabled" value="Advance Payment">Advance Payment</b-form-radio>
                                            <b-form-radio value="Full Payment">Full Payment</b-form-radio>
                                        </b-form-radio-group>
                                    </b-form-group>

                                    <b-form-group v-if="billPaymentType == 'Advance Payment'">
                                        <label class="mt-2" for="input-bill-amount-advance">Advance Amount
                                            (&#8377;):</label>
                                        <b-form-input id="input-bill-amount-advance" v-model="billAmount" required
                                            :state="billAmountState" aria-describedby="input-live-help input-live-feedback"
                                            placeholder="Enter Bill Advance Amount" trim></b-form-input>
                                        <!-- This will only be shown if the preceding input has an invalid state -->
                                        <b-form-invalid-feedback id="input-live-feedback">
                                            Enter a valid bill amount
                                        </b-form-invalid-feedback>
                                    </b-form-group>

                                    <b-form-group v-if="billPaymentType == 'Full Payment'">
                                        <label class="mt-2" for="input-bill-amount">Bill Total (&#8377;):</label>
                                        <b-form-input id="input-bill-amount" v-model="billAmount" required
                                            :state="billAmountState" aria-describedby="input-live-help input-live-feedback"
                                            placeholder="Enter Bill Amount" trim></b-form-input>
                                        <!-- This will only be shown if the preceding input has an invalid state -->
                                        <b-form-invalid-feedback id="input-live-feedback">
                                            Enter a valid bill total
                                        </b-form-invalid-feedback>
                                    </b-form-group>


                                    <b-form-group>
                                        <label for="input-bill-gst-number" class="mt-2">Bill GST Number:</label>
                                        <b-form-input id="input-bill-gst-number" v-model="billGstNumber"
                                            :state="billGstNumberState"
                                            aria-describedby="input-live-help input-live-feedback"
                                            placeholder="Enter Bill GST Number" trim></b-form-input>

                                        <!-- This will only be shown if the preceding input has an invalid state -->
                                        <b-form-invalid-feedback id="input-live-feedback">
                                            Enter a valid bill GST number
                                        </b-form-invalid-feedback>
                                    </b-form-group>

                                    <b-form-group v-if="billPaymentType == 'Advance Payment'">
                                        <label for="input-bill-description" class="mt-2">Bill Description: (mention
                                            advance
                                            amount %)</label>
                                        <b-form-textarea id="input-bill-description" v-model="billDescription" required
                                            :state="advanceBillDescriptionState"
                                            placeholder="Enter Bill Description with advance %" rows="3"
                                            aria-describedby="input-live-help input-live-feedback"
                                            max-rows="6"></b-form-textarea>
                                    </b-form-group>

                                    <!-- This will only be shown if the preceding input has an invalid state -->
                                    <b-form-invalid-feedback id="input-live-feedback">
                                        Enter a valid bill description with advance %
                                    </b-form-invalid-feedback>

                                    <b-form-group v-if="billPaymentType == 'Full Payment'">
                                        <label for="input-bill-description" class="mt-2">Bill Description:</label>
                                        <b-form-textarea id="textarea" v-model="billDescription" required
                                            placeholder="Enter Bill Description" rows="3" max-rows="6"></b-form-textarea>
                                    </b-form-group>

                                    <b-form-group>
                                        <label class="mt-2" for="input-bill-amount-text">Bill Amount in Words (&#8377;):</label>
                                        <b-form-input id="input-bill-amount-text" v-model="billAmountText" required
                                            :state="billAmountTextState"
                                            aria-describedby="input-live-help input-live-feedback"
                                            placeholder="Enter Bill Amount in Words" trim></b-form-input>
                                        <!-- This will only be shown if the preceding input has an invalid state -->
                                        <b-form-invalid-feedback id="input-live-feedback">
                                            Enter a valid bill total in words
                                        </b-form-invalid-feedback>
                                    </b-form-group>

                                    <b-form-file class="mt-3" v-model="billImage" :state="Boolean(billImage)"
                                        placeholder="Choose a file or drop it here..." accept=".pdf" required
                                        drop-placeholder="Drop file here..."></b-form-file>
                                    <div class="mt-3">Selected file: {{ billImage ? billImage.name : '' }}</div>
                                </div>
                            </b-card>
                        </div>
                    </b-col>
                </b-row>
                <b-button v-if="!isSubmitting" class="mt-3" type="submit" variant="primary">
                    Submit Bill
                </b-button>
                <b-button v-if="isSubmitting" class="mt-3" disabled variant="primary">
                    <b-spinner small type="grow"></b-spinner>
                    Submitting...
                </b-button>
            </b-form>
        </b-card>
    </b-container>
</template>

<script>
import axios from 'axios';
import config from '@/config';
import departmentData from '@/departmentEmail.json';
export default {
    data() {
        return {
            pocName: null,
            pocNameState: null,
            eventName: null,
            eventNameState: null,
            pocPhone: null,
            pocPhoneState: null,
            accHolderName: null,
            accHolderNameState: null,
            accNumber: null,
            accNumberState: null,
            ifscCode: null,
            ifscCodeState: null,
            bankName: null,
            bankNameState: null,
            branchName: null,
            billNumber: null,
            billDate: null,
            billType: null,
            vendorName: null,
            vendorNameState: null,
            vendorAddress: null,
            billGstNumber: null,
            billGstNumberState: null,
            billDescription: null,
            advanceBillDescriptionState: null,
            billPaymentType: null,
            billAmount: null,
            billAmountState: null,
            billAmountText: null,
            billAmountTextState: null,
            billImage: null,
            isSubmitting: false,
            departmentCategory: null,
            departmentOptions: [
                { value: null, text: 'Please select an Event/Department' },
                {
                    label: 'Departments',
                    options: [
                        { value: 'Facilities & Requirements', text: 'Facilites & Requirements' },
                        { value: 'Accommodation & Mess', text: 'Accommodation & Mess' },
                        { value: 'Photography & Videography', text: 'Photography & Videography' },
                        { value: 'Sponsorship', text: 'Sponsorship' },
                        { value: 'Hospitality', text: 'Hospitality' },
                        { value: 'Sales & Merchandise', text: 'Sales & Merchandise' },
                        { value: 'Student Relations', text: 'Student Relations' },
                        { value: 'Design & Content', text: 'Design & Content' },
                        { value: 'Publicity & PR', text: 'PR & Publicity' },
                        { value: 'Security', text: 'Security' },
                        { value: 'WebOps', text: 'WebOps' },
                        { value: 'Finance', text: 'Finance' },
                    ],
                },
                {
                    label: 'Events',
                    options: [
                        { value: 'Culturals', text: 'Culturals' },
                        { value: 'Sports', text: 'Sports' },
                        { value: 'Professionals', text: 'Professionals' },
                        { value: 'Technicals', text: 'Technicals' },
                    ]
                }
            ]
        }
    },
    methods: {
        validateNumber(number) {
            return /^\d+$/.test(number);
        },
        validateIfscCode(ifsc) {
            return /^[A-Z]{4}0[A-Z0-9]{6}$/.test(ifsc);
        },
        validateName(name) {
            return /^[a-zA-Z ]+$/.test(name);
        },
        validatePocPhone(phone) {
            return /^[6-9]\d{9}$/.test(phone);
        },
        validateGst(gst) {
            return /\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}/.test(gst);
        },
        validateBillAmount(amount) {
            return /^\d+(\.\d{1,2})?$/.test(amount);
        },
        validateBillAmountText(amount) {
            return /^[a-zA-Z ]+$/.test(amount);
        },
        async onSubmit(event) {
            event.preventDefault();
            this.isSubmitting = true;

            // if (this.billType == 'Student Reimbursement') {
            //     if (this.pocNameState && this.pocPhoneState && this.billNumberState && this.vendorNameState && this.billGstNumberState && this.advanceBillDescriptionState && this.billAmountState && this.billAmountTextState) {
            //         console.log(this.pocNameState, this.pocPhoneState, this.vendorNameState, this.billGstNumberState, this.advanceBillDescriptionState, this.billAmountState, this.billAmountTextState)
            //     }
            //     else {
            //         console.log(this.pocNameState, this.pocPhoneState, this.vendorNameState, this.billGstNumberState, this.advanceBillDescriptionState, this.billAmountState, this.billAmountTextState)
            //         this.$bvToast.toast('Please fill all the required fields', {
            //         title: 'Error',
            //         variant: 'danger',
            //         solid: true,
            //     });
            //     this.isSubmitting = false;
            //     console.log('error error error')
            //     }
            // }

            // console.log(this.pocNameState, this.eventNameState, this.pocPhoneState, this.accHolderNameState, this.accNumberState, this.ifscCodeState, this.bankNameState, this.billNumberState, this.vendorNameState, this.billGstNumberState, this.advanceBillDescriptionState, this.billAmountState, this.billAmountTextState)
            if (!this.pocNameState && !this.eventNameState && !this.pocPhoneState && !this.accHolderNameState && !this.accNumberState && !this.ifscCodeState && !this.bankNameState && !this.billNumberState && !this.vendorNameState && !this.billGstNumberState && !this.advanceBillDescriptionState && !this.billAmountState && !this.billAmountTextState) {
                this.$bvToast.toast('Please fill all the required fields', {
                    title: 'Error',
                    variant: 'danger',
                    solid: true,
                });
                this.isSubmitting = false;
                console.log('error error error')
            }

            else {
                const email = departmentData.find(item => item.Department === this.departmentCategory).Email;

                var formData = new FormData();
                formData.append('poc_name', this.pocName);
                formData.append('poc_email', email);
                formData.append('event_name', this.eventName);
                formData.append('poc_phone', this.pocPhone);
                formData.append('bill_department', this.departmentCategory);
                formData.append('bill_number', this.billNumber);
                formData.append('bill_date', this.billDate);
                formData.append('bill_type', this.billType);
                formData.append('vendor_name', this.vendorName);
                formData.append('vendor_address', this.vendorAddress);
                formData.append('gst_number', this.billGstNumber);
                formData.append('bill_payment_type', this.billPaymentType)
                formData.append('bill_description', this.billDescription);
                formData.append('bill_amount', this.billAmount);
                formData.append('bill_amount_in_words', this.billAmountText);
                formData.append('bill_image', this.billImage);
                formData.append('acc_holder_name', this.accHolderName);
                formData.append('acc_number', this.accNumber);
                formData.append('ifsc_code', this.ifscCode);
                formData.append('bank_name', this.bankName);
                formData.append('branch_name', this.branchName);

                await axios.post(`${config.API_BASE_URL}/bills`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }).then((res) => {
                    this.isSubmitting = false;
                    if(res.data.success) 
                        this.$router.push('/bill-success');
                    else if(!res.data.success)
                        this.$bvToast.toast('Bill Number Already Exists!', {
                            title: 'Error',
                            variant: 'danger',
                            solid: true,
                        });
                }).catch((error) => {
                    console.log(error);
                    this.isSubmitting = false;
                }
                );
            }
        },
    },
    computed: {
        isAdvancePaymentDisabled() {
            return this.billType !== 'Vendor Payment';
        },
    },
    watch: {
        pocName(val) {
            if (this.validateName(val)) {
                this.pocNameState = true;
            } else if (!this.validateName(val)){
                this.pocNameState = false;
            } else {
                this.pocNameState = null;
            }
        },
        eventName(val) {
            if (val.length < 1) {
                this.eventNameState = null;
                return;
            } else if (val.length > 3) {
                this.eventNameState = true;
            } else {
                this.eventNameState = false;
            }
        },
        pocPhone(val) {
            if (val.length < 1) {
                this.pocPhoneState = null;
                return;
            } else if (this.validatePocPhone(val)) {
                this.pocPhoneState = true;
            } else {
                this.pocPhoneState = false;
            }
        },
        accHolderName(val) {
            if (val.length < 1) {
                this.accHolderNameState = null;
                return;
            } else if (this.validateName(val)) {
                this.accHolderNameState = true;
            } else {
                this.accHolderNameState = false;
            }
            console.log(this.accHolderNameState)
        },
        accNumber(val) {
            if (val.length < 1) {
                this.accNumberState = null;
                return;
            } else if (this.validateNumber(val)) {
                this.accNumberState = true;
            } else {
                this.accNumberState = false;
            }
        },
        ifscCode(val) {
            if (val.length < 1) {
                this.ifscCodeState = null;
                return;
            } else if (this.validateIfscCode(val)) {
                this.ifscCodeState = true;
            } else {
                this.ifscCodeState = false;
            }
        },
        bankName(val) {
            if (val.length < 1) {
                this.bankNameState = null;
                return;
            } else if (val.length > 3) {
                this.bankNameState = true;
            } else {
                this.bankNameState = false;
            }
        },
        vendorName(val) {
            if (val.length < 1) {
                this.vendorNameState = null;
                return;
            } else if (val.length > 3) {
                this.vendorNameState = true;
            } else {
                this.vendorNameState = false;
            }
        },
        billGstNumber(val) {
            if (val.length < 1) {
                this.billGstNumberState = null;
                return;
            } else if (this.validateGst(val)) {
                this.billGstNumberState = true;
            } else {
                this.billGstNumberState = false;
            }
        },
        billDescription(val) {
            if (val.length < 1) {
                this.advanceBillDescriptionState = null;
                return;
            } else if (val.includes('%')) {
                this.advanceBillDescriptionState = true;
            } else {
                this.advanceBillDescriptionState = false;
            }
        },
        billAmount(val) {
            if (val.length < 1) {
                this.billAmountState = null;
                return;
            } else if (this.validateBillAmount(val)) {
                this.billAmountState = true;
            } else {
                this.billAmountState = false;
            }
        },
        billAmountText(val) {
            if (val.length < 1) {
                this.billAmountTextState = null;
                return;
            } else if (this.validateBillAmountText(val)) {
                this.billAmountTextState = true;
            } else {
                this.billAmountTextState = false;
            }
        },
    }
}
</script>

<style scoped>
.poc-info-card {
    max-width: 600px;
}

.bill-details-card {
    width: 600px;
}
</style>