// SPDX-License-Identifier: MIT
pragma solidity >=0.8.7;

contract ModelStorage {
    // string loss_fn;
    // string optimizer;


    struct Model {
        string model_ipfs;
        uint256 accuracy;
        address author;
    }


    Model[] models;


    constructor(
        string memory model_init_ipfs,
        // string memory loss_fn_,
        // string memory optimizer_,
        uint256 model_init_accuracy
    ) {
        // loss_fn = loss_fn_;
        // optimizer = optimizer_;
        Model memory tmp = Model({
            model_ipfs: model_init_ipfs,
            accuracy: model_init_accuracy,
            author: msg.sender
        });
        models.push(tmp);
    }


    function submit_model_weight(
        string memory current_model,
        uint256 accuracy_
    ) public {
        Model memory submit_ = Model({
            model_ipfs: current_model,
            accuracy: accuracy_,
            author: msg.sender
        });

        models.push(submit_);
    }


    // function get_loss_function() public view returns (string memory) {
    //     return loss_fn;
    // }


    // function get_optimizer() public view returns (string memory) {
    //     return optimizer;
    // }


    function get_latest_model_ipfs()
        public
        view
        returns (string memory)
    {
        return models[models.length - 1].model_ipfs;
    }


    function get_all_round() public view returns (Model[] memory) {
        return models;
    }
}
