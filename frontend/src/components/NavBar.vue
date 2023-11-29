<template>
    <b-navbar class="custom-navbar" toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#">Finance-Paradox</b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown right>
                    <!-- Using 'button-content' slot -->
                    <template #button-content>
                        <em>{{ user_data.name }}</em>
                    </template>
                    <b-dropdown-item @click="signOut">Sign Out</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>

<script>
export default {
    name: 'NavBar',
    props: {
        user_data: {
            type: Object,
            required: true,
        },
    },
    methods: {
        signOut() {
            localStorage.removeItem('token');
            this.$router.push({ name: 'login' });
        },
    },
}
</script>

<style>
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    width: 100%;
}
</style>