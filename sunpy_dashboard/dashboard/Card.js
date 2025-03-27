import PackageView from './PackageView.js'

export default {
    props: ['package'],
    components: {
        PackageView
    },
    methods: {
        statusBackground(status) {
            return {
                'has-background-success': status == 'succeeded',
                'has-background-warning': status == 'out-of-date',
                'has-background-danger': status == 'failed',
            };
        },
    },
    template: `
        <div class="card large">
            <div class="card-content">
                <div class="media">
                    <div class="media-left" v-if="package.logo">
                        <figure class="image is-48x48">
                            <img :src="package.logo" alt="Image">
                        </figure>
                    </div>
                    <div class="media-content">
                        <p class="title no-padding"><a class="has-text-grey-darker" :href="package.repourl">{{package.name}}</a></p>
                        <p :title="package.last_release" class="subtitle no-padding">{{package.version}}</p>
                    </div>
                </div>
                <PackageView v-for="branch in package.active_branches"
                             :name="package.name"
                             :branch="branch"/>
            </div>
        </div>
    `
}
