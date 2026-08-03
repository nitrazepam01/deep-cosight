function matlab_runner(requestPath, responsePath)
request = jsondecode(fileread(requestPath));
plant = request.plant;
if strcmp(plant.representation, 'transfer_function')
    if strcmp(plant.timebase.kind, 'discrete')
        system = tf(plant.numerator(:).', plant.denominator(:).', plant.timebase.dt);
    else
        system = tf(plant.numerator(:).', plant.denominator(:).');
    end
    if isfield(request.controller, 'representation') && strcmp(request.controller.representation, 'transfer_function')
        model = request.controller.model;
        if isfield(model, 'dt') && ~isempty(model.dt)
            controller = tf(model.numerator(:).', model.denominator(:).', model.dt);
        else
            controller = tf(model.numerator(:).', model.denominator(:).');
        end
    else
        controller = tf(1, 1);
    end
    loop = minreal(controller * system);
    if strcmp(request.configuration, 'open_loop')
        responseSystem = loop;
    else
        signValue = -1;
        if strcmp(request.feedback.sign, 'positive')
            signValue = 1;
        end
        responseSystem = feedback(loop, request.feedback.gain, signValue);
    end
else
    if strcmp(plant.timebase.kind, 'discrete')
        system = ss(plant.A, plant.B, plant.C, plant.D, plant.timebase.dt);
    else
        system = ss(plant.A, plant.B, plant.C, plant.D);
    end
    responseSystem = system;
    if strcmp(request.configuration, 'closed_loop') && isfield(request.controller, 'representation') && strcmp(request.controller.representation, 'state_feedback')
        K = request.controller.gain_matrix;
        referenceGain = 1;
        if isfield(request.controller, 'reference_gain')
            referenceGain = request.controller.reference_gain;
        end
        responseSystem = ss(system.A - system.B * K, system.B * referenceGain, system.C, system.D * referenceGain, system.Ts);
    end
end
[stepValues, stepTime] = step(responseSystem, request.time(:));
poles = pole(responseSystem);
result = struct( ...
    'backend', 'matlab', ...
    'available', true, ...
    'step_time', stepTime(:).', ...
    'step_values', squeeze(stepValues).', ...
    'poles_real', real(poles(:)).', ...
    'poles_imag', imag(poles(:)).');
handle = fopen(responsePath, 'w');
if handle < 0
    error('Unable to open response path');
end
cleanup = onCleanup(@() fclose(handle));
fwrite(handle, jsonencode(result), 'char');
end
