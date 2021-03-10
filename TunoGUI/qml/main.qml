import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import "controls"

Window {
    id: window
    width: 900
    height: 500
    opacity: 1
    visible: true
    color: "#00000000"
    title: qsTr("TUno")

    Rectangle {
        id: form
        color: "#00000000"
        border.color: "#18314f"
        border.width: 0
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0

        Rectangle {
            id: maincontainer
            color: "#00000000"
            anchors.fill: parent

            Rectangle {
                id: bg
                color: "#121615"
                border.width: 2
                anchors.fill: parent
            }

            Rectangle {
                id: topcontainer
                height: 50
                color: "#000000"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0


                Rectangle {
                    id: rightcontainer
                    width: 150
                    height: 0
                    color: "#00000000"
                    border.color: "#a30000"
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    Row {
                        id: rowButtons
                        anchors.fill: parent

                        TopButton {
                            id: minimizebtn
                            colorPressed: "#5f7470"
                        }

                        TopButton {
                            id: maximizebtn
                            colorPressed: "#5f7470"
                            btnIconSource: "../Images/svg_images/maximize_icon.svg"
                        }

                        TopButton {
                            id: closebtn
                            btnIconSource: "../Images/svg_images/close_icon.svg"
                        }
                    }
                }



                Rectangle {
                    id: middleContaienr
                    color: "#00000000"
                    anchors.left: lefttopcontainer.right
                    anchors.right: rightcontainer.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0

                    Label {
                        id: label
                        color: "#f5f5f5"
                        text: qsTr("TUno")
                        anchors.fill: parent
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 12
                        styleColor: "#f5f5f5"
                    }
                }

                Rectangle {
                    id: lefttopcontainer
                    width: 50
                    color: "#00000000"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    CustomToggleBtn {
                        id: customToggleBtn
                        anchors.fill: parent
                        colorPressed: "#5f7470"
                    }
                }

            }
        }
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:8}D{i:9}D{i:6}D{i:5}D{i:11}D{i:10}D{i:13}D{i:12}
}
##^##*/
