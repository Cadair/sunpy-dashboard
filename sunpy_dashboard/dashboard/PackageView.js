export default {
    data() {
        return {
            build: [],
        };
    },
    props: [
        'name',
        'branch',
    ],
    computed: {
        buildId() {
            return `${this.name}${this.branch}`;
        }
    },
    mounted() {
        var self = this;
        $.getJSON(`/api/latest_build/${self.name}/${self.branch}`, function(data) {
            self.build = data;
            console.log(self.build.status);
        });
    },
    methods: {
        statusBackground(status) {
            return {
                'has-background-success': status == 'succeeded',
                'has-background-warning': status == 'out-of-date',
                'has-background-danger': status == 'failed',
            };
        },
        toggleJob(package_, branch) {
            let jobEl = document.getElementById(`${package_}${branch}`);
            jobEl.style.display = jobEl.style.display == "none" ? "block" : "none";
        },
    },
    template: `
        <div @click="toggleJob(name, branch)">
            <p class="branch-box subtitle mb-0 has-text-weight-bold has-text-black-ter box" :class="statusBackground(build.status)">{{branch}}</p>
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
        </div>
    `
}
