import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15
import "controls"

Window {
    id: window
    width: 900
    height: 500
    opacity: 1
    visible: true
    color: "#00000000"
    title: qsTr("TUno")

    flags: Qt.Window | Qt.FramelessWindowHint

    Rectangle {
        id: form
        color: "#00000000"
        border.color: "#141414"
        border.width: 2
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
            visible: true
            color: "#00000000"
            border.color: "#a30000"
            border.width: 2
            anchors.fill: parent
            anchors.rightMargin: 2
            anchors.leftMargin: 2
            anchors.bottomMargin: 2
            anchors.topMargin: 2

            Rectangle {
                id: bg
                color: "#121615"
                border.color: "#a30000"
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

                    DragHandler {
                        onActiveChanged: if(active){
                                             window.startSystemMove()
                                         }
                    }

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
                        onClicked: animationMenu.running = true
                    }
                }

            }


            Rectangle {
                id: sidecontainer
                x: 0
                width: 50
                color: "#000000"
                border.color: "#121615"
                anchors.top: topcontainer.bottom
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.topMargin: 0

                PropertyAnimation {
                    id: animationMenu
                    target: sidecontainer
                    property: "width"
                    to: if (sidecontainer.width == 50)
                            return 200;
                        else
                            return 50
                    duration: 350
                    easing.type: Easing.OutQuint
                }

                Column {
                    id: sideButtons
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    spacing: 10
                    anchors.bottomMargin: 65
                    anchors.topMargin: 40

                    SideButton {
                        id: sideButton
                        width: sidecontainer.width
                        active: true
                    }

                    SideButton {
                        id: sideButton1
                        width: sidecontainer.width
                        text: "Join game"
                        btnIconSource: "../Images/svg_images/save_icon.svg"
                    }

                    SideButton {
                        id: sideButton2
                        width: sidecontainer.width
                        visible: true
                        text: "Profile"
                        btnIconSource: "../Images/svg_images/resize_icon.svg"
                        spacing: 6
                    }
                }

                SideButton {
                    id: sideButton3
                    x: 0
                    y: 190
                    width: sidecontainer.width
                    visible: true
                    text: "Settings"
                    anchors.bottom: parent.bottom
                    clip: true
                    anchors.bottomMargin: 25
                    btnIconSource: "../Images/svg_images/settings_icon.svg"
                    spacing: 6
                }
            }
            Rectangle {
                id: contentcontainer
                color: "#121615"
                anchors.left: sidecontainer.right
                anchors.right: parent.right
                anchors.top: topcontainer.bottom
                anchors.bottom: parent.bottom
                anchors.leftMargin: 0
                anchors.topMargin: 0
            }
        }
    }
}





/*##^##
Designer {
    D{i:0;formeditorZoom:0.9}
}
##^##*/
