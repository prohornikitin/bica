package com.example.bica

package object utils {
    type Feelings = Array[Float]
    type FeelingsImmutable = Seq[Float]

    def updateActorAppraisal(actorAppraisal: Array[Float], effectOnActor: Seq[Float], r: Float = 0.1): Unit = {
        assert(actorAppraisal.length == effectOnActor.length)
        for (i <- actorAppraisal.indices) {
            val newAppraisal = (1-r) * actorAppraisal(i) + r * effectOnActor(i)
            actorAppraisal.update(i, newAppraisal)
        }
    }
}
