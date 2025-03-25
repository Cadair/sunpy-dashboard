export default {
    props: [
        'name',
        'branch',
        'build',
    ],
    computed: {
        buildId() {
            return `${name}${this.branch}`;
        }
    },
    template: `
        <p class="subtitle mb-0 has-text-weight-bold has-text-black-ter">{{branch}}</p>
        <div style="display: none;" :id="buildId">
            <div class="mt-2" :title="build.time" v-for="build in build.builds">
                <p class="has-text-weight-bold">{{build.service_name}}</p>
                <ul class="pl-5 has-text-weight-bold has-text-black-ter" style="list-style-type: circle;">
                    <li :class="statusBackground(job.status)" v-for="job in build.jobs">
                        <a :href="build.url">{{job.name}}</a>
                    </li>
                </ul>
            </div>
        </div>
    `
}
