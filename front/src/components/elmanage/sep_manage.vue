<template>
    <div class="cardview">
        <div class="cardview_body">
            <div class="mcr-head">
                <h4>该部分用于对未来几天的可申请预约时段的分配工作,请根据实际情况合理分配</h4>
                <hr>
                <div>
                    <div class="text=-center">&nbsp;&nbsp;<strong>请注意如下说明：</strong></div><br>
                    <div class="text-start">
                        1.本部分中，你可以选择每天的申请最大数量限制、分配可用的时段，以及申请的时段长度。管理的最早日期为距今三天后，最多可管理七天的时间分配。请留意公司安排、节假日和其他特殊情况。
                        <strong>已经提交的申请数据不受此部分的约束。</strong>
                    </div>
                    <div class="text-start">2.本部分用于管理每个小时段的可申请状。例如，如果时间段长度设置为了三个小时，且选中了
                        <button type="button" class="btn btn-primary btn-sm disabled" data-bs-toggle="button"
                            autocomplete="off">○ - 08:00 -></button>，
                        且此后两个时刻的按钮显示为<button type="button" class="btn btn-warning btn-sm disabled"
                            data-bs-toggle="button" autocomplete="off">○ - 09:00 -></button>和
                        <button type="button" class="btn btn-warning btn-sm disabled" data-bs-toggle="button"
                            autocomplete="off">○ - 10:00 -></button>。
                        这表示<p class="mcr-p">九点和十点不能作为预约起始时刻</p>，但所有用户将可以选择<p class="mcr-p">起始时间</p>为八点这一时刻的预约时间段，
                        并在此后的三个小时进行认证并通过。时间长短取决于你的<p class="mcr-p">时段长度</p>的分配。
                    </div>
                    <div class="text-start">3.一般情况下，系统会提供默认的时段分配，如果没有显示默认值，请手动分配。
                    </div>
                    <div class="text-start">4.最大预约数量默认为无限制。即没有选择或选择无限制的情况下，都将认为不对预约申请数量作出限制。</div>
                </div>
            </div>
            <div class="mcr-inval"></div>
            <div class="mcr-head">
                <div class="text-start">
                    <h3>&nbsp;&nbsp;快速管理（对接下来的几天使用同一设定）</h3>
                    <div class="text-end mcr-mein"><strong style="color:red">!请注意，这可能会覆盖此前的设定&nbsp;&nbsp;</strong>
                    </div><br>
                </div>
                <timeset0 :key=0 :number=0 />
                <br>
            </div>

            <div class="mcr-inval"></div>

            <div class="mcr-cont">
                <div class="accordion" id="accordionExample">

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingOne">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                                对 <p class="mcr-p" id="mcr-date0">{{ getDate(3) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseOne" class="accordion-collapse collapse" aria-labelledby="headingOne"
                            data-bs-parent="#accordionExample" style="">
                            <div class="accordion-body">
                                <hr>
                                <timeset1 :key=1 :number=1 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingTwo">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                对 <p class="mcr-p" id="mcr-date1">{{ getDate(4) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo"
                            data-bs-parent="#accordionExample" style="">
                            <div class="accordion-body">
                                <hr>
                                <timeset2 :key=2 :number=2 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingThree">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                对 <p class="mcr-p" id="mcr-date2">{{ getDate(5) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseThree" class="accordion-collapse collapse" aria-labelledby="headingThree"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <hr>
                                <timeset3 :key=3 :number=3 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingFour">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                                对 <p class="mcr-p" id="mcr-date3">{{ getDate(6) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseFour" class="accordion-collapse collapse" aria-labelledby="headingFour"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <hr>
                                <timeset4 :key=4 :number=4 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingFive">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
                                对 <p class="mcr-p" id="mcr-date4">{{ getDate(7) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseFive" class="accordion-collapse collapse" aria-labelledby="headingFive"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <hr>
                                <timeset5 :key=5 :number=5 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingSix">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseSix" aria-expanded="false" aria-controls="collapseSix">
                                对 <p class="mcr-p" id="mcr-date5">{{ getDate(8) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseSix" class="accordion-collapse collapse" aria-labelledby="headingSix"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <hr>
                                <timeset6 :key=6 :number=6 />
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="headingSeven">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#collapseSeven" aria-expanded="false" aria-controls="collapseSeven">
                                对 <p class="mcr-p" id="mcr-date6">{{ getDate(9) }}</p> 的可申请预约时段分配
                            </button>
                        </h2>
                        <div id="collapseSeven" class="accordion-collapse collapse" aria-labelledby="headingSeven"
                            data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <hr>
                                <timeset7 :key=7 :number=7 />
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
    

</template>
<script>
import timeset0 from "@/components/elmanage/timeset.vue";
import timeset1 from "@/components/elmanage/timeset.vue";
import timeset2 from "@/components/elmanage/timeset.vue";
import timeset3 from "@/components/elmanage/timeset.vue";
import timeset4 from "@/components/elmanage/timeset.vue";
import timeset5 from "@/components/elmanage/timeset.vue";
import timeset6 from "@/components/elmanage/timeset.vue";
import timeset7 from "@/components/elmanage/timeset.vue";

export default {
    components: { timeset0, timeset1, timeset2, timeset3, timeset4, timeset5, timeset6, timeset7 },
    methods: {
        
        getDate(daysAhead) {
            const today = new Date();
            const targetDate = new Date(today);
            targetDate.setDate(today.getDate() + daysAhead);

            const year = targetDate.getFullYear();
            const month = String(targetDate.getMonth() + 1).padStart(2, '0'); // 月份从0开始
            const day = String(targetDate.getDate()).padStart(2, '0');
            const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
            const weekDay = weekDays[targetDate.getDay()];

            return `${year}-${month}-${day} ${weekDay}`;
        }
    }
}
</script>